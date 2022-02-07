<template>
  <div>
    <b-field label="Username">
      <b-input v-model='username'></b-input>
    </b-field>
    <b-field label="Password">
      <b-input type="password" v-model='password'></b-input>
    </b-field>
    <b-button @click='submitLogin'>Login</b-button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    submitLogin() {
      this.$http.post('/login', {username: this.username, password: this.password}).then((response) => {
        const token = response.data.access_token;
        const user = response.data.user;
        this.$store.commit('setAuth', {token, user});

        const postLoginUrl = this.$route.query.redirect || '/'
        this.$router.push({path: postLoginUrl});
      });
    }
  }
}
</script>