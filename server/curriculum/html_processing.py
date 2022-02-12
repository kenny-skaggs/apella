from abc import ABC, abstractmethod
from enum import Enum
import json

from bs4 import BeautifulSoup, Tag
from flask import render_template

from curriculum import schema, model, repository
from responses import repository as responses_repository


class RenderTarget(Enum):
    AUTHORING = 1
    TEACHING = 2
    RESPONDING = 3


class _HtmlProcessor(ABC):
    def process_html(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')

        node_func_map = {
            'question_choice': self._process_choice_node,
            'question_paragraph': self._process_paragraph_node,
            'question_inline_text': self._process_inline_text_node,
            'question_inline_dropdown': self._process_inline_dropdown_node
        }

        question_nodes = soup.find_all(class_='wysiwyg_question')
        for node in question_nodes:
            question_class = next(class_name for class_name in node['class'] if class_name in node_func_map)
            node_func_map[question_class](node)

        return soup.prettify()

    @abstractmethod
    def _process_choice_node(self, node):
        ...

    @abstractmethod
    def _process_paragraph_node(self, node):
        ...

    @abstractmethod
    def _process_inline_text_node(self, node):
        ...

    @abstractmethod
    def _process_inline_dropdown_node(self, node):
        ...

    @classmethod
    def _set_question_id(cls, node: Tag, question_id: int):
        node['question_id'] = question_id

    @classmethod
    def _get_question_id(cls, node: Tag):
        return node.get('question_id')


class LessonRenderer(_HtmlProcessor):
    def __init__(self, render_target: RenderTarget):
        self.render_target = render_target
        self.question_answer_map = {}

    def process_html(self, html: str, user_id: int, lesson_id: int):
        if self.render_target == RenderTarget.AUTHORING:
            return html

        if self.render_target == RenderTarget.RESPONDING:
            self.question_answer_map = responses_repository.AnswerRepository.user_answer_map_for_lesson(
                user_id=user_id,
                lesson_id=lesson_id
            )
            # TODO: use question ids to populate answers when loading

        return super(LessonRenderer, self).process_html(html)

    def _process_choice_node(self, node: Tag):
        question_id = self._get_question_id(node)
        answer = self.question_answer_map.get(int(question_id))
        display_html = render_template(
            'response_fields/multiple_choice.html',
            question_id=question_id,
            answer=answer
        )
        display_html = BeautifulSoup(display_html, 'html.parser')
        node.replace_with(next(iter(display_html)))

    def _process_paragraph_node(self, node: Tag):
        question_id = self._get_question_id(node)
        answer = self.question_answer_map.get(int(question_id))
        display_html = render_template(
            'response_fields/paragraph_text.html',
            question_id=question_id,
            answer=answer
        )
        display_html = BeautifulSoup(display_html, 'html.parser')
        node.replace_with(next(iter(display_html)))

    def _process_inline_text_node(self, node: Tag):
        question_id = self._get_question_id(node)
        answer = self.question_answer_map.get(int(question_id))
        display_html = render_template(
            'response_fields/inline_text.html',
            question_id=question_id,
            answer=answer
        )
        display_html = BeautifulSoup(display_html, 'html.parser')
        node.replace_with(next(iter(display_html)))

    def _process_inline_dropdown_node(self, node: Tag):
        question_id = self._get_question_id(node)
        answer = self.question_answer_map.get(int(question_id))
        print(answer)
        option_list = json.loads(node['options'])
        display_html = render_template(
            'response_fields/inline_select.html',
            options=option_list,
            question_id=question_id,
            answer=answer
        )
        display_html = BeautifulSoup(display_html, 'html.parser')
        node.replace_with(next(iter(display_html)))


class QuestionParser(_HtmlProcessor):
    """Responsible for going through any lesson html that is being saved to upsert any question data from the html"""

    def __init__(self, page_id: int):
        self.page_id = page_id
        self.id_resolution_map = {
            'questions': {},
            'options': {}
        }

    def _process_choice_node(self, node):
        option_list = json.loads(node['options'])
        question = self._build_question(
            _id=self._get_question_id(node),
            _type=schema.QuestionType.CHOICE,
        )
        question.options = [
            model.Option(id=option['id'], text=option['html'])
            for option in option_list
        ]

        question = self._upsert_and_finalize(question=question, node=node)

        for index, option in enumerate(option_list):
            if str(option['id']).startswith('temp-option-'):
                self.id_resolution_map['options'][option['id']] = question.options[index].id
        node['options'] = json.dumps([
            {'id': option.id, 'html': option.text}
            for option in question.options
        ])

    def _process_paragraph_node(self, node):
        question = self._build_question(
            _id=self._get_question_id(node),
            _type=schema.QuestionType.PARAGRAPH,
        )

        self._upsert_and_finalize(question=question, node=node)

    def _process_inline_text_node(self, node):
        question = self._build_question(
            _id=self._get_question_id(node),
            _type=schema.QuestionType.INLINE_TEXT,
        )

        self._upsert_and_finalize(question=question, node=node)

    def _process_inline_dropdown_node(self, node):
        option_list = json.loads(node['options'])
        question = self._build_question(
            _id=self._get_question_id(node),
            _type=schema.QuestionType.INLINE_DROPDOWN,
        )
        question.options = [
            model.Option(id=None, text=option.get('text'))
            for option in option_list
        ]

        question = self._upsert_and_finalize(question=question, node=node)

        node['options'] = json.dumps([
            {'text': option.text, 'id': option.id}
            for option in question.options
        ])

    def _upsert_and_finalize(self, question: model.Question, node: Tag):
        question = repository.QuestionRepository.upsert(question)
        self._set_question_id(node, question.id)

        if 'temp-id' in node.attrs:
            self.id_resolution_map['questions'][node.attrs['temp-id']] = question.id
            del node.attrs['temp-id']

        return question

    def _build_question(self, _id: int, _type: schema.QuestionType):
        return model.Question(
            id=_id,
            type=_type,
            page_id=self.page_id
        )
