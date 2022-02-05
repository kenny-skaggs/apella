<template>
  <div id="app">
    navbar here
    <router-view></router-view>
    <b-loading v-model='showLoading'></b-loading>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    showLoading() {
      return this.$store.state.isLoading;
    }
  }
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/bulmaswatch.scss"

#app .loading-overlay .loading-background
  background: rgba($background, 0.5)
</style>
