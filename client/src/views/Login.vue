<template>
    <div>
        <b-field label="Username">
            <b-input v-model='username'></b-input>
        </b-field>
        <b-field label="Password">
            <b-input type="password" v-model='password'></b-input>
        </b-field>
        <b-button @click='submitLogin'>Login</b-button>
        <hr>
        <div id="google-signin"/>
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
            this.$http.post(
                '/login',
                {username: this.username, password: this.password}
            ).then(this.onAuthSuccess);
        },
        onAuthSuccess(response) {
            const token = response.data.access_token;
            const user = response.data.user;
            this.$store.commit('setAuth', {token, user});

            const postLoginUrl = this.$route.query.redirect || '/'
            this.$router.push({path: postLoginUrl});
        }
    },
    created() {
        const vueThis = this;
        window.handleCredentialResponse = (response) => {
            vueThis.$http.post('/google-login', {
                token: response.credential
            }).then(vueThis.onAuthSuccess);
            // TODO: handle 404 error when account not found
        }
    },
    mounted() {
        google.accounts.id.initialize({
            client_id: "1053916245539-n962ukgl4kd058vggq4g5kf5gts8e3oo.apps.googleusercontent.com",
            callback: handleCredentialResponse
        });
        google.accounts.id.renderButton(
            document.getElementById('google-signin'),
            {
                type: "standard",
                size: "large",
                theme: "outline",
                text: "sign_in_with",
                shape: "rectangular",
                logo_alignment: "left"
            }
        )
    }
}
</script>