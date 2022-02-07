<template>
  <div class="pageNavigator">
    <div class="pageItem" :class='{selected: page.id === selectedPageId}'
         v-for='page in pages' :key='page.id' @click='pageClicked(page)'>
      <span>{{ page.name }}</span>
      <b-tag v-if='editable' rounded type="is-danger" @click.stop.prevent='$emit("deletePage", page.id)'>
        &cross;
      </b-tag>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LessonPageNavigation',
  props: ['pages', 'selectedPageId', 'editable'],
  methods: {
    pageClicked(page) {
      this.$emit('pageClicked', page);
    }
  }
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/variables"

.pageNavigator
  border-right: 1px white solid

.pageItem
  display: flex
  justify-content: center
  align-items: center

  min-height: 4em
  border-bottom: 1px white solid

  &:hover
    cursor: pointer
    background: $grey-dark

  &.selected
    background: $grey


</style>
