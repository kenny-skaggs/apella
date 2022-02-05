import json

from bs4 import BeautifulSoup
from flask import render_template


class LessonHtmlPreRenderer:
    @classmethod
    def pre_render(cls, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        node_builder_map = {
            'question_choice': cls.build_multiple_choice,
            'question_paragraph': cls.build_paragraph,
            'question_inline_text': cls.build_inline_short,
            'question_inline_dropdown': cls.build_inline_dropdown
        }

        question_nodes = soup.find_all(class_='wysiwyg_question')
        for node in question_nodes:
            question_class = next(class_name for class_name in node['class'] if class_name in node_builder_map)
            display_html = node_builder_map[question_class](node)
            display_html = BeautifulSoup(display_html, 'html.parser')
            node.replace_with(next(iter(display_html)))

        return soup.prettify()

    @classmethod
    def build_multiple_choice(cls, _):
        return render_template('response_fields/multiple_choice.html')

    @classmethod
    def build_paragraph(cls, _):
        return render_template('response_fields/paragraph_text.html')

    @classmethod
    def build_inline_short(cls, _):
        return render_template('response_fields/inline_text.html')

    @classmethod
    def build_inline_dropdown(cls, node):
        option_list = json.loads(node['options'])
        return render_template('response_fields/inline_select.html', options=option_list)
