<template>
  <div class="curriculum-tile">
    <b-button class="edit-button" icon-pack="fas" icon-left="edit"
              v-if='editable' @click.stop='editClicked'>
    </b-button>
    <span>
      <slot></slot>
    </span>
  </div>
</template>

<script>
export default {
  name: 'Tile',
  methods: {
    editClicked() {
      this.$emit('edit');
    }
  },
  props: ['editable']
}
</script>

<style lang="sass">
@import "../../../node_modules/bulmaswatch/darkly/variables"
.curriculum-tile
  position: relative

  width: 15em
  height: 8em
  background-color: $grey
  margin: 2em
  border-radius: 1em

  display: flex
  align-items: center
  justify-content: center

  &:hover
    background-color: $grey-lighter
    cursor: pointer
    color: #333

.edit-button
  position: absolute
  right: 1em
  top: 1em
</style>
