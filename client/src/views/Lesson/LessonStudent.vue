<template>
    <div v-html='lessonHtml' class="student-view"/>
</template>

<script>
import DebounceMixin from "../../mixins/DebounceMixin";

export default {
    name: 'LessonStudent',
    methods: {
        answerSelected(questionId, answer, submitted, $questionElement) {
            this.debounce(questionId, () => {
                this.$socket.client.emit('response_provided', {
                    questionId: questionId,
                    answer: answer,
                    submitted: submitted,
                    auth: this.$store.state.authToken
                }, () => {
                    if (submitted) {
                        $questionElement.addClass('locked');
                        $questionElement.find('.submit-btn').attr('disabled', 'disabled');
                        $questionElement.find('.inline-submit').attr('disabled', 'disabled');
                        $questionElement.find('textarea').attr('disabled', 'disabled');
                        $questionElement.find('input').attr('disabled', 'disabled');
                    }
                });
            });
        },
        sendChoiceAnswer($questionElement, submitAnswer) {
            const questionId = $questionElement.attr('questionId');

            // TODO: when submitting an answer, need to display something if it fails

            const answerIds = $questionElement.find('.question-choice.selected').map((index, element) => $(element).attr('option-id'));
            this.answerSelected(questionId, answerIds.get(), submitAnswer, $questionElement);
        }
    },
    created() {
        $('body').on('response-input', (event, answer) => {
            const $target = $(event.target);
            this.answerSelected($target.attr('questionId'), answer, false);

            // TODO: need to be able to submit paragraph, short answer, and dropdown selection
        });

        $('body').on('click', '.apella-question.paragraph .submit-btn', ({target}) => {
            const $questionElement = $(target).closest('.apella-question');
            const questionId = $questionElement.attr('questionId');
            const $textAreaInput = $questionElement.find('textarea');

            this.answerSelected(questionId, $textAreaInput.val(), true, $questionElement);
        });

        $('body').on('click', '.apella-inline.text .inline-submit', ({target}) => {
            const $container = $(target).closest('.apella-inline');
            const $input = $container.find('input');

            this.answerSelected($input.attr('questionid'), $input.val(), true, $container);
        });

        // $('body').on('click', '.apella-inline.dropdown .inline-submit', ({target}) => {
        //     const $container = $(target).closest('.apella-inline');
        //     const $input = $container.find('select');
        //
        //     this.answerSelected($input.attr('questionid'), $input.val(), true);
        // });

        $('body').on('click', '.apella-question.choice .question-choice', ({target}) => {
            $(target).closest('.question-choice').toggleClass('selected');
            this.sendChoiceAnswer($(target).closest('.apella-question'), false);
        });
        $('body').on('click', '.apella-question.choice .submit-btn', ({target}) => {
            this.sendChoiceAnswer($(target).closest('.apella-question'), true);
        });

        $('body').on('click', '.apella-question.rubric .submit-btn', ({target}) => {
            const $questionElement = $(target).closest('.apella-question');
            const questionId = $questionElement.attr('questionId');
            const projectInput = $questionElement.find('.rubric-input');

            this.answerSelected(questionId, projectInput.val(), true, $questionElement);
        })
    },
    mounted() {
        this.$socket.client.connect();
    },
    props: ['lessonHtml'],
    mixins: [DebounceMixin]
}
</script>

<style lang="sass">
@import "~bulmaswatch/flatly/variables"

.student-view
    .apella-question
        border: 1px solid $grey

    .apella-question.choice
        .question-choice
            &.selected
                border: 1px solid $grey
                margin: calc(0.5em - 1px)

        &:not(.locked)
            .question-choice:hover
                background: $grey
                cursor: pointer

    td
        padding: 0.4em

</style>
