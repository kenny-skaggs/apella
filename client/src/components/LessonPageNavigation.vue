<template>
  <draggable :list='pages' class="pageNavigator" handle=".move-control" @change='pageOrderChanged' :animation='100'>
    <div class="pageItem" :class='{selected: page.id === selectedPageId}'
         v-for='page in pages' :key='page.id' @click='pageClicked(page)'>
      <div class="editing-control move-control" v-if='editable'>
        <b-icon pack="fas" icon="grip-lines"></b-icon>
      </div>
      <span class="name">{{ page.name }}</span>
      <div class="editing-control">
        <b-tag v-if='editable' rounded type="is-danger" @click.stop.prevent='$emit("deletePage", page.id)'>
          &cross;
        </b-tag>
      </div>
    </div>
  </draggable>
</template>

<script>
import draggable from "vuedraggable";
import AuthCheckMixin from "../mixins/AuthCheckMixin";

export default {
  name: 'LessonPageNavigation',
  props: ['pages', 'selectedPageId', 'editable', 'lessonId'],
  methods: {
    pageClicked(page) {
      this.$emit('pageClicked', page);
    },
    pageOrderChanged() {
      const ordered_page_ids = this.pages.map((page) => page.id);
      this.$http.post(`/curriculum/lesson/order/${this.lessonId}`, {pageIds: ordered_page_ids});
    }
  },
  components: {draggable},
  mixins: [AuthCheckMixin]
}
</script>

<style lang="sass">
@import "~bulmaswatch/flatly/variables"
@import "@/my-colors.sass"

.pageNavigator
  border-right: 1px $low-contrast solid

.pageItem
  display: flex
  align-items: center
  justify-content: space-between

  min-height: 4em
  border-bottom: 1px $low-contrast solid

  &:hover
    cursor: pointer
    background: $low-contrast

  &.selected
    background: $grey

  .name
    flex-grow: 1
    padding-left: 0.5em

  .editing-control
    margin: 0.5em

    &.move-control
      cursor: move


</style>
