<template>
    <div>
        <em v-if='isSaveQueued' class="save-notification">Saving...</em>
        <em v-else class="save-notification">Saved</em>

        <b-field label="Name">
            <b-input v-model='selectedPage.name'></b-input>
        </b-field>
        <HtmlEditor v-model='lessonHtml' :page-id='selectedPage.id' :allowQuestionInsert='true'
                    @questionClicked='questionClicked'/>
        <b-button @click='saveHtmlToServer'>
            Save to Server
        </b-button>
        <b-button @click='modifyClicked'>Modify</b-button>
        <b-modal v-model='showChoiceModal'>
            <div>Edit Choices</div>
            <div class="rich-option-editor" v-for='option in options' :key='option.id'>
                <html-editor v-model='option.html'/>
                <b-button class="is-small" type="is-danger" @click="removeOption(option)">Delete</b-button>
            </div>
            <b-button @click='addChoiceClicked'>Add Choice</b-button>
            <div class="buttons">
                <b-button type="is-success" @click='submitChoices'>Save</b-button>
                <b-button @click='closeChoiceModal'>Cancel</b-button>
            </div>
        </b-modal>
        <RubricModal :show-modal='showRubricModal' :rubricItems='rubricItems' @saveRubric='saveRubric' />
    </div>
</template>

<script>
import HtmlEditor from "../../components/editor/HtmlEditor";
import RubricModal from "../../components/editor/RubricModal";

export default {
    props: ['selectedPage', 'value'],
    data() {
        return {
            editingQuestion: undefined,
            showChoiceModal: false,
            showRubricModal: false,
            options: [],
            rubricItems: undefined,
            tempOptionId: 1,
            queuedSaveToServer: undefined
        }
    },
    methods: {
        questionClicked(questionElement) {
            let $questionElement = $(questionElement);
            this.editingQuestion = questionElement;

            if ($questionElement.hasClass('question_choice')) {
                const serializedOptions = $questionElement.attr('options');
                this.options = JSON.parse(serializedOptions);
                this.showChoiceModal = true;
            } else if ($questionElement.hasClass('question_rubric')) {
                this.rubricItems = JSON.parse($questionElement.attr('rubric-items'));
                this.showRubricModal = true;
            }
        },
        addChoiceClicked() {
            this.options.push({id: `temp-option-${this.tempOptionId++}`, html: ''})
        },
        removeOption(option) {
            this.options = this.options.filter((o) => o.id !== option.id);
        },
        modifyClicked() {
            this.showChoiceModal = true;
        },
        submitChoices() {
            const $element = $(this.editingQuestion);
            const trumbowyg_core = $element.closest('.trumbowyg-editor').data('trumbowyg');
            $(this.editingQuestion).attr('options', JSON.stringify(this.options));
            trumbowyg_core.$c.trigger('tbwchange');
            this.closeChoiceModal();
        },
        closeChoiceModal() {
            this.showChoiceModal = false;
        },
        saveRubric() {
            const $element = $(this.editingQuestion);
            this.showRubricModal = false;
            $(this.editingQuestion).attr('rubric-items', JSON.stringify(this.rubricItems));
            const trumbowyg_core = $element.closest('.trumbowyg-editor').data('trumbowyg');
            trumbowyg_core.$c.trigger('tbwchange');
        },
        queueSave() {
            if (this.queuedSaveToServer !== undefined) {
                clearTimeout(this.queuedSaveToServer);
            }

            this.queuedSaveToServer = setTimeout(() => {
                this.queuedSaveToServer = undefined;
                this.saveHtmlToServer();
            }, 1500);
        },
        saveHtmlToServer() {
            this.$http.post('/curriculum/pages', this.selectedPage).then((response) => {
                // TODO: there's got to be a way to get this encapsulated in the HtmlEditor (maybe a prop for the map?)
                const resolution_map = response.data.id_resolution;
                $('.wysiwyg_question[temp-id]').each((i, node) => {
                    const $node = $(node);
                    const tempId = $node.attr('temp-id');
                    const newId = resolution_map['questions'][tempId];
                    $node.attr('questionId', newId);
                    $node.removeAttr('temp-id');
                });
                $('.wysiwyg_question[options]').each((i, node) => {
                    const $node = $(node);
                    const options = JSON.parse($node.attr('options'));
                    options.forEach((option) => {
                        if (option.id.toString().startsWith('temp-option')) {
                            const tempId = option.id;
                            option.id = resolution_map['options'][tempId]
                        }
                    });
                    $node.attr('options', JSON.stringify(options));
                });
                Object.keys(resolution_map['rubric_items']).forEach((questionId) => {
                    const itemIds = resolution_map['rubric_items'][questionId];
                    const $question = $(`.wysiwyg_question[question_id="${questionId}"]`);
                    const rubricJsonList = JSON.parse($question.attr('rubric-items'));
                    rubricJsonList.forEach((item, index) => {
                        item.id = itemIds[index];
                    });

                    $question.attr('rubric-items', JSON.stringify(rubricJsonList));
                });
            });
        }
    },
    computed: {
        lessonHtml: {
            get() {
                return this.value;
            },
            set(newValue) {
                this.$emit('input', newValue);
                this.queueSave();
            }
        },
        isSaveQueued() {
            return this.queuedSaveToServer !== undefined;
        }
    },
    components: {HtmlEditor, RubricModal}
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/_variables.scss"

.wysiwyg_question
    border: 1px solid $grey-dark
    border-radius: 5px
    padding: 5px

    &:hover
        cursor: pointer
        background: $grey-dark

.trumbowyg-modal
    color: #333

.rich-option-editor
    margin: 2em

    .trumbowyg-box, .trumbowyg .trumbowyg-editor
        min-height: 7em

.save-notification
    color: $grey-light
    position: absolute
    right: 0

</style>
