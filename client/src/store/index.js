import Vue from 'vue';
import Vuex from 'vuex';
import VuexPersistence from 'vuex-persist';

Vue.use(Vuex);

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
})

export default new Vuex.Store({
    state: {
        isLoading: false,
        authToken: undefined,
        user: undefined,
        selectedClassId: undefined,
        uniqueId: 0,
        toast: undefined,

        activeCourse: undefined,
        activeUnit: undefined,
        activeLesson: undefined,

        renderLessonAsTeacher: false,
        viewAsPdCourse: false
    },
    mutations: {
        setIsLoading (state, loading) {
            state.isLoading = loading;
        },
        setAuth (state, {token, user}) {
            state.authToken = token;
            state.user = user;
        },
        clearState (state) {
            state.authToken = undefined;
            state.user = undefined;
            state.selectedClassId = undefined;

            state.activeCourse = undefined;
            state.activeUnit = undefined;
            state.activeLesson = undefined;

            state.renderLessonAsTeacher = false;
            state.viewAsPdCourse = false;
        },
        setSelectedClass (state, class_id) {
            state.selectedClassId = class_id
        },
        showToast (state, toast) {
            state.toast = toast;
        },
        setActiveCourse (state, course) {
            state.activeCourse = course;
            state.activeUnit = undefined;
            state.activeLesson = undefined;
        },
        setActiveUnit (state, unit) {
            state.activeUnit = unit;
            state.activeLesson = undefined;
        },
        setActiveLesson (state, lesson) {
            state.activeLesson = lesson;
        },
        clearCurrentCourse(state) {
            state.activeCourse = undefined;
            state.activeUnit = undefined;
            state.activeLesson = undefined;
        },
        clearCurrentUnit(state) {
            state.activeUnit = undefined;
            state.activeLesson = undefined;
        },
        clearCurrentLesson(state){
            state.activeLesson = undefined;
        },
        setRenderAsTeacher(state, renderAsTeacher){
            state.renderLessonAsTeacher = renderAsTeacher;
        },
        setViewAsPdCourse(state, viewAsPdCourse) {
            state.viewAsPdCourse = viewAsPdCourse;
        }
    },
    getters: {
        userHasRole: (state) => (role) => {
            const user = state.user;
            if (user === undefined) {
                return false;
            } else {
                return user.roles.find((user_role) => user_role === role) !== undefined;
            }
        },
        nextUniqueId: (state) => () => {
            return `apella-element-${state.uniqueId++}`;
        }
    },
    actions: {
    },
    modules: {
    },
    plugins: [vuexLocal.plugin]
});
