export default {
    computed: {
        userIsAuthor() {
            return this.$store.getters.userHasRole('author');
        }
    }
}
