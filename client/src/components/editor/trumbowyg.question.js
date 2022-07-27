const buildPlugin = function ($) {
    'use strict';
    let next_temp_id = 0;

    const question_options = [
        {
            id: 'question_choice',
            display: 'Multiple Choice Question',
            template: '<p options="[]">Options for a multiple choice question will appear here.</p>'
        },
        {
            id: 'question_paragraph',
            display: 'Paragraph Answer',
            template: '<p>Student will have a large text box to enter text here.</p>'
        },
        {
            id: 'question_inline_text',
            display: 'Short Answer',
            template: '<span>A small field to enter text will appear here</span>'
        },
        // {
        //     id: 'question_inline_dropdown',
        //     display: 'Inline Dropdown',
        //     template: '<span options="[]">A dropdown field to select an option will appear here</span>'
        // },
        {
            id: 'question_rubric',
            display: 'Project Rubric',
            template: '<div rubric-items="[]">A project rubric will appear here.</div>'
        }
    ]

    question_options.forEach((option) => {
        $('body').on('click', '.wysiwyg_question.' + option.id, function (event) {
            const element = event.target;
            const trumbowyg_core = $(element).closest('.trumbowyg-editor').data('trumbowyg');

            trumbowyg_core.$c.trigger('question-clicked', element);
        });
    });

    function buildButtonDef (trumbowyg) {
        question_options.forEach((option) => {
            trumbowyg.addBtnDef(option.id, {
                text: option.display,
                hasIcon: false,
                fn: function () {
                    const $questionNode = $(option.template);
                    $questionNode.addClass('wysiwyg_question');
                    $questionNode.addClass(option.id);
                    $questionNode.attr('contenteditable', 'false');
                    $questionNode.attr('temp-id', next_temp_id++);

                    trumbowyg.saveRange();
                    // trumbowyg.range.deleteContents();
                    trumbowyg.range.insertNode($questionNode[0]);
                }
            });
        });
        return {
            dropdown: question_options.map((option) => option.id)
        }
    }

    $.extend(true, $.trumbowyg, {
        langs: {
            en: {
                question: 'Question Plugin'
            },
        },
        plugins: {
            question: {
                init: function (trumbowyg) {
                    trumbowyg.o.plugins.question = $.extend(
                        {}, {},
                        trumbowyg.o.plugins.question || {}
                    );
                    trumbowyg.addBtnDef('question', buildButtonDef(trumbowyg));
                }
            }
        }
    })
}

export default buildPlugin;
