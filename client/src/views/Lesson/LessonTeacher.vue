<template>
  <div>
    <div v-html='lessonHtml' />
    <div id="viz" />
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'LessonTeacher',
  props: ['lessonHtml', 'pageId'],
  mounted() {
    d3.select("#viz").append("span").text("Hello d3");
  },
  watch: {
    pageId() {
      this.$http.get(`/responses/${this.pageId}`)
    }
  }
}
</script>
