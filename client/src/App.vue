<template>
  <div id="app">
    <b-navbar>
      <template #brand>
        <b-navbar-item><strong>Apella</strong></b-navbar-item>
      </template>
      <template #end v-if='isLoggedIn'>
        <b-navbar-dropdown>
          <template #label>
            <b-icon pack="fas" icon="user"></b-icon>
            <span>{{ user.username }}</span>
          </template>
          <b-navbar-item href="#" @click='logoutClicked'>
            Logout
          </b-navbar-item>
        </b-navbar-dropdown>
      </template>
    </b-navbar>
    <router-view></router-view>
    <b-loading v-model='showLoading'></b-loading>
  </div>
</template>

<script>
export default {
  name: 'App',
  created() {
    this.$http.interceptors.request.use((config) => {
      const token = this.$store.state.authToken;
      if (token !== undefined) {
        config.headers['Authorization'] = 'Bearer' + token;
      }
      return config;
    });
    this.$http.interceptors.response.use((event) => event,
        (event) => {
          if (event.response.status === 401 && !event.request.responseURL.endsWith('/login')) {
            this.$router.push({name: 'login', query: { redirect: this.$route.path }})
          } else {
            return event;
          }
        }
    )
  },
  methods: {
    logoutClicked() {
      this.$store.commit('clearAuth');
      this.$router.push({name: 'login'});
    }
  },
  computed: {
    showLoading() {
      return this.$store.state.isLoading;
    },
    isLoggedIn() {
      return this.$store.state.user !== undefined;
    },
    user() {
      return this.$store.state.user;
    }
  }
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/bulmaswatch.scss"

#app .loading-overlay .loading-background
  background: rgba($background, 0.5)
</style>
