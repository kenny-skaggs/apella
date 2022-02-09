<template>
  <div v-html='lessonHtml' />
</template>

<script>
export default {
  name: 'LessonStudent',
  methods: {
    answerSelected(questionId, answer) {

      this.$socket.emit('response_provided', {
        questionId: questionId,
        answer: answer
      });
    }
  },
  created() {
    $('body').on('response-input', (event, answer) => {
      const $target = $(event.target);
      this.answerSelected($target.attr('questionId'), answer);
    })
  },
  props: ['lessonHtml']
}
</script>
