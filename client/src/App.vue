<template>
    <div id="app">
        <b-navbar class="apella-navbar">
            <template #brand>
                <b-navbar-item :href='$router.resolve({ name: "dashboard" }).href'><strong>Apella</strong>
                </b-navbar-item>
            </template>
            <template #start>
                <b-navbar-item v-if='shouldViewAuthorControls'
                               :href='$router.resolve({ name: "school_management" }).href'>
                    Schools
                </b-navbar-item>
                <b-navbar-item v-if='shouldViewTeachingControls'
                               :href='$router.resolve({ name: "class_management" }).href'>
                    Classes
                </b-navbar-item>
                <b-navbar-item class="nav-bar-logo">
                </b-navbar-item>
            </template>
            <template #end v-if='isLoggedIn'>
                <b-navbar-item v-if='shouldViewTeachingControls'>
                    <ClassSelector/>
                </b-navbar-item>
                <b-navbar-item v-if='userIsAuthor'>
                    <b-button @click='toggleTeacherView' v-if='$store.state.renderLessonAsTeacher'>Author View</b-button>
                    <b-button @click='toggleTeacherView' v-else>Teacher View</b-button>
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
        <b-breadcrumb>
            <template v-if='$store.state.activeCourse !== undefined'>
                <b-breadcrumb-item
                    tag='router-link'
                    :to="{name: 'course_detail', params: {courseId: $store.state.activeCourse.id}}"
                    :active='$store.state.activeUnit === undefined'
                >
                    {{ $store.state.activeCourse.name }}
                </b-breadcrumb-item>
            </template>
            <template v-if='$store.state.activeUnit !== undefined'>
                <b-breadcrumb-item
                    tag='router-link'
                    :to="{name: 'unit_detail', params: {unitId: $store.state.activeUnit.id}}"
                    :active='$store.state.activeLesson === undefined'
                >
                    {{ $store.state.activeUnit.name }}
                </b-breadcrumb-item>
            </template>
            <template v-if='$store.state.activeLesson !== undefined'>
                <b-breadcrumb-item
                    tag='router-link'
                    :to="{name: 'lesson_detail', params: {lessonId: $store.state.activeLesson.id}}"
                    active
                >
                    {{ $store.state.activeLesson.name }}
                </b-breadcrumb-item>
            </template>
        </b-breadcrumb>
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
            this.$store.commit('clearState');
            this.$router.push({name: 'login'});

            // TODO: need to disconnect from socket server
        },
        showToast(toast) {
            this.$buefy.toast.open({
                message: toast.message,
                type: 'is-danger',
                position: 'is-bottom'
            })
        },
        toggleTeacherView() {
            this.$store.commit('setRenderAsTeacher', !this.$store.state.renderLessonAsTeacher);
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
@import "~bulmaswatch/flatly/bulmaswatch.scss"
@import "@/my-colors.sass"


#app
    font-size: 18px

    .apella-navbar
        border-radius: 0
        background-color: #082539

    .nav-bar-logo
        position: absolute
        top: 5px
        left: 30%
        right: 30%
        bottom: 5px

        background-image: url('http://localhost:5000/static/images/republic-logo-blue.jpeg')
        background-repeat: no-repeat
        background-position: center
        background-size: auto 90%

    .loading-overlay .loading-background
        background: rgba($background, 0.5)

.flex-row
    display: flex
    flex-direction: row
    align-items: center

.selection-container
    max-height: 70%
    overflow: scroll
    margin: 2em

.selectable-row
    display: flex
    align-items: center
    padding: 1em
    min-height: 4em
    border-bottom: 1px $low-contrast solid

    &:hover:not(.no-hover)
        cursor: pointer
        background: $low-contrast

.modal
    color: white !important

    label.label
        color: white


</style>
