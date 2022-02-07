from abc import ABC, abstractmethod
from enum import Enum
import json

from bs4 import BeautifulSoup, Tag
from flask import render_template

from storage import repository
from curriculum import models, view_models


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


class LessonRenderer(_HtmlProcessor):
    def __init__(self, render_target: RenderTarget):
        self.render_target = render_target

    def process_html(self, html: str):
        if self.render_target == RenderTarget.AUTHORING:
            return html
        else:
            return super(LessonRenderer, self).process_html(html)

    def _process_choice_node(self, node):
        display_html = render_template('response_fields/multiple_choice.html')
        display_html = BeautifulSoup(display_html, 'html.parser')
        node.replace_with(next(iter(display_html)))

    def _process_paragraph_node(self, node):
        display_html = render_template('response_fields/paragraph_text.html')
        display_html = BeautifulSoup(display_html, 'html.parser')
        node.replace_with(next(iter(display_html)))

    def _process_inline_text_node(self, node):
        display_html = render_template('response_fields/inline_text.html')
        display_html = BeautifulSoup(display_html, 'html.parser')
        node.replace_with(next(iter(display_html)))

    def _process_inline_dropdown_node(self, node):
        option_list = json.loads(node['options'])
        display_html = render_template('response_fields/inline_select.html', options=option_list)
        display_html = BeautifulSoup(display_html, 'html.parser')
        node.replace_with(next(iter(display_html)))


class QuestionParser(_HtmlProcessor):
    """Responsible for going through any lesson html that is being saved to upsert any question data from the html"""

    def __init__(self, page_id: int):
        self.page_id = page_id
        self.id_resolution_map = {}

    def _process_choice_node(self, node):
        option_list = json.loads(node['options'])
        question = self._build_question(
            _id=self._get_question_id(node),
            _type=models.QuestionType.CHOICE,
        )
        question.options = [
            view_models.Option(id=None, text=option)
            for option in option_list
        ]

        self._upsert_and_finalize(question=question, node=node)

    def _process_paragraph_node(self, node):
        question = self._build_question(
            _id=self._get_question_id(node),
            _type=models.QuestionType.PARAGRAPH,
        )

        self._upsert_and_finalize(question=question, node=node)

    def _process_inline_text_node(self, node):
        question = self._build_question(
            _id=self._get_question_id(node),
            _type=models.QuestionType.INLINE_TEXT,
        )

        self._upsert_and_finalize(question=question, node=node)

    def _process_inline_dropdown_node(self, node):
        option_list = json.loads(node['options'])
        question = self._build_question(
            _id=self._get_question_id(node),
            _type=models.QuestionType.INLINE_DROPDOWN,
        )
        question.options = [
            view_models.Option(id=None, text=option.get('text'))
            for option in option_list
        ]

        question = self._upsert_and_finalize(question=question, node=node)
        node['options'] = json.dumps([
            {'text': option.text, 'id': option.id}
            for option in question.options
        ])

    def _upsert_and_finalize(self, question: view_models.Question, node: Tag):
        question = repository.QuestionRepository.upsert(question)
        self._set_question_id(node, question.id)

        if 'temp-id' in node.attrs:
            self.id_resolution_map[node.attrs['temp-id']] = question.id
            del node.attrs['temp-id']

        return question

    def _build_question(self, _id: int, _type: models.QuestionType):
        return view_models.Question(
            id=_id,
            type=_type,
            page_id=self.page_id
        )

    @classmethod
    def _set_question_id(cls, node: Tag, question_id: int):
        node['question_id'] = question_id

    @classmethod
    def _get_question_id(cls, node: Tag):
        return node.get('question_id')
