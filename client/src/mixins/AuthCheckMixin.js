export default {
    computed: {
        userIsAuthor() {
            return this.$store.getters.userHasRole('author');
        },
        userIsTeacher() {
            return this.$store.getters.userHasRole('teacher');
        },
        userIsAuthorActingAsTeacher() {
            return this.$store.getters.userHasRole('author') && this.$store.state.renderLessonAsTeacher;
        },
        shouldViewTeachingControls() {
            return this.userIsTeacher || this.userIsAuthorActingAsTeacher;
        },
        shouldViewAuthorControls() {
            return this.userIsAuthor && !this.$store.state.renderLessonAsTeacher;
        }
    }
}
