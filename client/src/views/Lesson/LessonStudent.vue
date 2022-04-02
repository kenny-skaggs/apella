<template>
    <div v-html='lessonHtml' class="student-view"/>
</template>

<script>
export default {
    name: 'LessonStudent',
    methods: {
        answerSelected(questionId, answer) {

            this.$socket.client.emit('response_provided', {
                questionId: questionId,
                answer: answer
            });
        }
    },
    created() {
        $('body').on('response-input', (event, answer) => {
            const $target = $(event.target);
            this.answerSelected($target.attr('questionId'), answer);
        });
        $('body').on('click', '.apella-question.choice .question-choice', ({target}) => {
            const $questionElement = $(target).closest('.apella-question');
            const questionId = $questionElement.attr('questionId');
            $(target).closest('.question-choice').toggleClass('selected');

            const answerIds = $questionElement.find('.question-choice.selected').map((index, element) => $(element).attr('option-id'));
            this.answerSelected(questionId, answerIds.get());
        });
        $('body').on('click', '.apella-question.rubric .submit-btn', ({target}) => {
            const $questionElement = $(target).closest('.apella-question');
            const questionId = $questionElement.attr('questionId');
            const projectInput = $questionElement.find('.rubric-input');

            this.answerSelected(questionId, projectInput.val());
        })
    },
    mounted() {
        this.$socket.client.connect();
    },
    props: ['lessonHtml']
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/variables"

.student-view
    .apella-question
        border: 1px solid $grey

    .apella-question.choice
        .question-choice
            &.selected
                border: 1px solid $grey
                margin: calc(0.5em - 1px)

            &:hover
                background: $grey
                cursor: pointer

    td
        padding: 0.4em

</style>
