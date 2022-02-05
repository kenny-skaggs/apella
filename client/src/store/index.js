import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        isLoading: false
    },
    mutations: {
        setIsLoading (state, loading) {
            state.isLoading = loading;
        }
    },
    actions: {
    },
    modules: {
    },
});
