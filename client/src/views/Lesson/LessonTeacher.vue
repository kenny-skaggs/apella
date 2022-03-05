<template>
  <div v-html='lessonHtml' class="teacher-view" />
</template>

<script>
import lesson_utils from '@/utils/lesson.js';

export default {
  name: 'LessonTeacher',
  props: ['lessonHtml', 'pageId'],
  watch: {
    pageId() {
      this.retrieveResponses();
    }
  },
  methods: {
    retrieveResponses() {
      this.$http.get(`/responses/${this.pageId}`).then((response) => {
        lesson_utils.initializeDisplays(response.data);
      });
    }
  },
  mounted() {
    this.$socket.client.connect();

    this.$http.get(`/organization/class/${this.$store.state.selectedClassId}`).then((response) => {
      lesson_utils.initialize(response.data.students);

      if (this.pageId !== undefined) {
        this.retrieveResponses();
      }
    });
  },
  sockets: {
    newResponse(data) {
      lesson_utils.updateResponse(data.question_id, data);
    }
  }
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/variables"

.teacher-view
  .apella-question
    background: $grey-dark

    &:hover
      background: $grey
      cursor: pointer

  .chart-container
    position: relative

    label
      padding: 0.5em

    svg
      margin-top: 0.5em
      position: relative
      width: 10em
      height: 1em
      border: 1px solid $grey

  .apella-responses
    border: 1px solid $grey
    border-radius: 5px

    margin: 1em
    padding: 1em

    display: grid

    &.choice, &.inline-text, &.inline-select
      grid-template-columns: repeat(auto-fill, 12em)

    &.inline-select
      .option-display
        grid-column: 1 / -1

    .student-response
      margin: 0.3em
      border: 1px solid $grey

      .name
        margin: 0.5em

      &.choice
        display: flex
        align-items: stretch

        .name
          flex-grow: 1

        .selection
          padding: 0.5em
          background: $grey

          display: flex
          align-items: center

      &.paragraph
        .answer
          background: $grey
          border-radius: 5px
          margin: 0.5em
          padding: 0.5em

      &.inline-text, &.inline-select
        .answer
          background: $grey
          padding: 0.5em
</style>
