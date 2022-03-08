<template>
  <div id="app">
    <b-navbar>
      <template #brand>
        <b-navbar-item :href='$router.resolve({ name: "dashboard" }).href'><strong>Apella</strong></b-navbar-item>
      </template>
      <template #start>
        <b-navbar-item v-if='userIsTeacher' :href='$router.resolve({ name: "class_management" }).href'>Classes</b-navbar-item>
        <b-navbar-item v-if='userIsTeacher' :href='$router.resolve({ name: "account_management" }).href'>Accounts</b-navbar-item>
      </template>
      <template #end v-if='isLoggedIn'>
        <b-navbar-item v-if='userIsTeacher'>
          <ClassSelector />
        </b-navbar-item>
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
import AuthCheckMixin from "./mixins/AuthCheckMixin";
import ClassSelector from "./components/ClassSelector";
import toast from "./utils/toasts";

export default {
  name: 'App',
  components: {ClassSelector},
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
          const responseStatus = event.response.status;
          if (responseStatus === 401 && !event.request.responseURL.endsWith('/login')) {
            this.$router.push({name: 'login', query: {redirect: this.$route.path}});
          } else if (responseStatus === 403) {
            this.$store.commit(
                'showToast',
                toast.Toast(
                    "I'm sorry. You don't have permissions to do that.",
                    toast.level.error
                )
            );
            return Promise.reject(event);
          } else {
            return event;
          }
        }
    );

    const thisComponent = this;
    this.$store.watch(
        function (state) {
          return state.toast;
        },
        function (toast) {
          thisComponent.showToast(toast);
        }
    )
  },
  methods: {
    logoutClicked() {
      this.$store.commit('clearAuth');
      this.$router.push({name: 'login'});

      // TODO: need to disconnect from socket server
    },
    showToast(toast) {
      this.$buefy.toast.open({
        message: toast.message,
        type: 'is-danger',
        position: 'is-bottom'
      })
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
  },
  mixins: [AuthCheckMixin]
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/bulmaswatch.scss"

#app .loading-overlay .loading-background
  background: rgba($background, 0.5)
</style>
