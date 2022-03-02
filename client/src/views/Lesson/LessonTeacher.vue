<template>
  <div v-html='lessonHtml' class="teacher-view" />
</template>

<script>
import lesson_utils from '@/utils/lesson.js';

export default {
  name: 'LessonTeacher',
  props: ['lessonHtml', 'pageId'],
  sockets: {
    newResponse(data) {
      lesson_utils.updateResponse(data.question_id, data);
    }
  },
  watch: {
    pageId() {
      this.$http.get(`/responses/${this.pageId}`).then((response) => {
        lesson_utils.initializeDisplays(response.data);
      });
    }
  },
  mounted() {
    this.$socket.client.connect();
  }
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/variables"

.teacher-view
  .apella-question.choice:hover
    background: $grey
    cursor: pointer

  .chart-container
    position: relative

    svg
      margin-top: 0.5em
      position: relative
      width: 10em
      height: 1em
      border: 1px solid $grey
</style>
