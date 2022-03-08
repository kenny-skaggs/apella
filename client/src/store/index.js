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
        toast: undefined
    },
    mutations: {
        setIsLoading (state, loading) {
            state.isLoading = loading;
        },
        setAuth (state, {token, user}) {
            state.authToken = token;
            state.user = user;
        },
        clearAuth (state) {
            state.authToken = undefined;
            state.user = undefined;
        },
        setSelectedClass (state, class_id) {
            state.selectedClassId = class_id
        },
        showToast (state, toast) {
            state.toast = toast
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
