export default {
    computed: {
        userIsAuthor() {
            return this.$store.getters.userHasRole('author');
        },
        userIsTeacher() {
            return this.$store.getters.userHasRole('teacher');
        }
    }
}
