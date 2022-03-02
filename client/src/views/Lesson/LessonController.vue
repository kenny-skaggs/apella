<template>
  <div class="columns is-gapless">
    <div class="column is-2">
      <b-button @click='addNewPage' v-if='userIsAuthor'>Add Page</b-button>
      <PageNavigation :pages='pages' @pageClicked='pageSelected' :selected-page-id='selectedPageId'
          @deletePage='deletePage' :editable='userIsAuthor' :lesson-id='lessonId' />
    </div>
    <div class="column" v-if='selectedPage !== undefined'>
      <LessonAuthor v-if='userIsAuthor' :selected-page='selectedPage' v-model='selectedPage.html' />
      <LessonTeacher v-else-if='userIsTeacher' :lesson-html='selectedPage.html' :page-id='selectedPageId' />
      <LessonStudent v-else :lesson-html='selectedPage.html' />
    </div>
  </div>
</template>

<script>
import PageNavigation from '../../components/LessonPageNavigation.vue';
import AuthCheckMixin from "../../mixins/AuthCheckMixin";
import LessonStudent from "./LessonStudent";
import LessonTeacher from "./LessonTeacher";
import LessonAuthor from "./LessonAuthor";


export default {
  name: 'Lesson',
  methods: {
    pageSelected(page) {
      this.selectedPageId = page.id;
    },
    addNewPage() {
      this.pages.push({
        id: undefined,
        name: '',
        lesson_id: this.lessonId,
        html: ''
      })
    },
    deletePage(pageId) {
      const index = this.pages.findIndex((page) => page.id === pageId);
      if (index >= 0) {
        this.pages.splice(index, 1);
      }
    }
  },
  data() {
    return {
      selectedPageId: 1,
      pages: []
    }
  },
  created() {
    this.$http.get(`/curriculum/lesson/${this.lessonId}`).then((response) => {
      this.pages = response.data['pages'];
    });
  },
  computed: {
    selectedPage() {
      return this.pages.find((page) => page.id === this.selectedPageId);
    }
  },
  props: ['lessonId'],
  components: {
    LessonAuthor,
    LessonTeacher,
    LessonStudent,
    PageNavigation,
  },
  mixins: [AuthCheckMixin]
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/variables"

.apella-question.choice
  display: flex
  border-radius: 5px
  margin: 1em
  width: fit-content

  .question-choice
    margin: 0.5em
    padding: 1em
    border-radius: 0.5em

</style>
