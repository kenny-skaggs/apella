<template>
  <div class="columns is-gapless">
    <div class="column is-2">
      <b-button @click='addNewPage'>Add Page</b-button>
      <PageNavigation :pages='pages' @pageClicked='pageSelected' :selected-page-id='selectedPageId'
          @deletePage='deletePage' />
    </div>
    <div class="column">
      <b-field label="Name">
        <b-input v-model='selectedPage.name'></b-input>
      </b-field>
      <HtmlEditor v-model='selectedPage.html' :page-id='selectedPage.id' />
      <b-button @click='saveHtmlToServer'>
        Save to Server
      </b-button>
    </div>
  </div>
</template>

<script>
import PageNavigation from './LessonPageNavigation.vue';
import HtmlEditor from "./editor/HtmlEditor";

export default {
  name: 'Lesson',
  methods: {
    saveHtmlToServer() {
      // use debounce around the change event to save to the server
      this.$http.post('http://localhost:5000/curriculum/save', this.pages);
    },
    pageSelected(page) {
      this.selectedPageId = page.id;
    },
    addNewPage() {
      this.pages.push({
        id: Math.max(...this.pages.map((page) => page.id)) + 1,
        name: '',
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
      pages: [
        {id: 1, name: 'testone', html: '<p>bob one</p>'},
        {id: 2, name: 'testtwo', html: '<p>second</p>'},
        {id: 3, name: 'three', html: '<p>bhaoeu</p>'}
      ]
    }
  },
  mounted() {
    this.$http.get('http://localhost:5000/curriculum').then((response) => {
      this.pages = response.data;
    });
  },
  computed: {
    selectedPage() {
      return this.pages.find((page) => page.id === this.selectedPageId);
    }
  },
  components: {
    HtmlEditor,
    PageNavigation
  }
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/variables"

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
