const buildPlugin = function ($) {
    'use strict';
    let trumbowyg_core = undefined;
    let next_temp_id = 0;

    function saveTextOptionsToElement($modal, $element) {
        $element.attr('options', JSON.stringify($modal.find('input').map((i, el) => {
            return {text: el.value}
        }).get()));
    }

    function loadTextOptionsIntoModal($modal, $element) {
        let options = $element.attr('options');
        if (options !== undefined) {
            options = JSON.parse(options);
            $modal.find('input').each((i, input) => $(input).parent().remove());
            options.forEach((option) => $modal.find('section').append($('<p><input value="' + option.text + '" /></p>')))
        }
    }

    const question_options = [
        {
            id: 'question_choice',
            display: 'Multiple Choice Question',
            template: '<p>Options for a multiple choice question will appear here.</p>',
            modalContent: '<section><p><input /></p><p><input /></p><p><input /></p><p><input /></p></section>',
            modalLoad: function ($modal, $element) {
                loadTextOptionsIntoModal($modal, $element)
            },
            modalSubmit: function ($modal, $element) {
                saveTextOptionsToElement($modal, $element);
                trumbowyg_core.$c.trigger('tbwchange');
            }
        },
        {
            id: 'question_paragraph',
            display: 'Paragraph Answer',
            template: '<p>Student will have a large text box to enter text here.</p>'
        },
        {
            id: 'question_inline_text',
            display: 'Short Answer',
            template: '<span>a small field to enter text will appear here</span>'
        },
        {
            id: 'question_inline_dropdown',
            display: 'Inline Dropdown',
            template: '<span>a dropdown field to select an option will appear here</span>',
            modalContent: '<section><p><input /></p><p><input /></p><p><input /></p><p><input /></p></section>',
            modalLoad: function ($modal, $element) {
                loadTextOptionsIntoModal($modal, $element)
            },
            modalSubmit: function ($modal, $element) {
                saveTextOptionsToElement($modal, $element);
                trumbowyg_core.$c.trigger('tbwchange');
            }
        }
    ]

    question_options.forEach((option) => {
        $('body').on('click', '.wysiwyg_question.' + option.id, function (event) {
            const element = event.target;

            const $modal = trumbowyg_core.openModal(
                'Configure Response Field',
                option.modalContent || '' + '<p><button class="delete-question">Delete Question</button></p>'
            );

            $modal.on('click', '.delete-question', function (event) {
                event.preventDefault();
                element.remove();
                trumbowyg_core.$c.trigger('tbwchange');
                trumbowyg_core.closeModal();
            });

            $modal.on('tbwconfirm', function(e){
                e.preventDefault();
                trumbowyg_core.closeModal();
                if (option.modalSubmit) {
                    option.modalSubmit($modal, $(element));
                }
            });
            $modal.on('tbwcancel', function(e){
                trumbowyg_core.closeModal();
            });

            if (option.modalLoad) {
                option.modalLoad($modal, $(element));
            }
        });
    });

    function buildButtonDef (trumbowyg) {
        trumbowyg_core = trumbowyg;

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
