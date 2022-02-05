<template>
  <b-modal v-model='showModal'>
    <div>Edit Modal</div>
    <slot></slot>
    <div class="buttons">
      <b-button type="is-success" @click='submitModal'>Save</b-button>
      <b-button @click='closeModal'>Cancel</b-button>
    </div>
  </b-modal>
</template>

<script>
export default {
  props: ['showModal'],
  methods: {
    submitModal() {
      this.$emit('submit');
    },
    closeModal() {
      this.$emit('close');
    }
  }
}
</script>
