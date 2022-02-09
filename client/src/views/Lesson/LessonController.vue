<template>
  <div class="columns is-gapless">
    <div class="column is-2">
      <b-button @click='addNewPage' v-if='userIsAuthor'>Add Page</b-button>
      <PageNavigation :pages='pages' @pageClicked='pageSelected' :selected-page-id='selectedPageId'
          @deletePage='deletePage' :editable='userIsAuthor' />
    </div>
    <div class="column" v-if='selectedPage !== undefined'>
      <template v-if='userIsAuthor'>
        <b-field label="Name">
          <b-input v-model='selectedPage.name'></b-input>
        </b-field>
        <HtmlEditor v-model='selectedPage.html' :page-id='selectedPage.id' />
        <b-button @click='saveHtmlToServer'>
          Save to Server
        </b-button>
      </template>
      <template v-else>
        <LessonStudent :lesson-html='selectedPage.html' />
      </template>
    </div>
  </div>
</template>

<script>
import PageNavigation from '../../components/LessonPageNavigation.vue';
import HtmlEditor from "../../components/editor/HtmlEditor";
import AuthCheckMixin from "../../mixins/AuthCheckMixin";
import LessonStudent from "./LessonStudent";


export default {
  name: 'Lesson',
  methods: {
    saveHtmlToServer() {
      // use debounce around the change event to save to the server
      this.$http.post('/curriculum/pages', this.selectedPage).then((response) => {
        // TODO: there's got to be a way to get this encapsulated in the HtmlEditor (maybe a prop for the map?)
        const resolution_map = response.data.id_resolution;
        $('.wysiwyg_question[temp-id]').each((i, node) => {
          const $node = $(node);
          const tempId = $node.attr('temp-id');
          const newId = resolution_map[tempId];
          $node.attr('questionId', newId);
          $node.removeAttr('temp-id');
        })
      });
    },
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
    HtmlEditor,
    LessonStudent,
    PageNavigation,
  },
  mixins: [AuthCheckMixin]
}
</script>

<style lang="sass">
@import "../../../node_modules/bulmaswatch/darkly/variables"

.wysiwyg_question
  border: 1px solid $grey-dark
  border-radius: 5px
  padding: 5px

  &:hover
    cursor: pointer
    background: $grey-dark

.trumbowyg-modal
  color: #333
</style>
