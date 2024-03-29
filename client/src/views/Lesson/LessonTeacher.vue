<template>
    <div>
        <div v-html='lessonHtml' class="teacher-view"/>
        <RubricModal v-model='showRubric'
                     :rubric-items='currentRubricItems'
                     :student-map='currentStudentMap'
                     :response-map='currentResponseMap'
                     @lockResponse='setResponseLocked'
        />
    </div>
</template>

<script>
import lesson_utils from '@/utils/lesson.js';
import RubricModal from "./teacher/RubricModal";

export default {
    name: 'LessonTeacher',
    props: ['lessonHtml', 'pageId'],
    data() {
        return {
            showRubric: false,
            currentRubricItems: undefined,
            currentResponseMap: undefined,
            currentStudentMap: undefined
        }
    },
    watch: {
        pageId() {
            this.retrieveResponses();
        }
    },
    methods: {
        retrieveResponses() {
            this.$http.get(`/responses/${this.pageId}`).then((response) => {
                lesson_utils.initializeDisplays(response.data);
            });
        },
        showRubricModal() {
            this.showRubric = true;
        },
        rubricDetailsSelected(questionId, rubricItems, responseMap, studentMap) {
            this.currentRubricItems = rubricItems;
            this.showRubric = true;
            this.currentResponseMap = responseMap;
            this.currentStudentMap = studentMap;
        },
        setResponseLocked(responseId, setLocked, successCallback) {
            this.$http.post('/responses/lock', {
                responseId: responseId,
                locked: setLocked
            }).then(successCallback);
        }
    },
    mounted() {
        this.$socket.$subscribe('connect', () => {
            this.$socket.client.emit('identify', {
                auth: this.$store.state.authToken
            });
        });
        this.$socket.client.connect();

        this.$http.get(`/organization/class/${this.$store.state.selectedClassId}`).then((response) => {
            lesson_utils.initialize(response.data.students, this, this.setResponseLocked);

            if (this.pageId !== undefined) {
                this.retrieveResponses();
            }
        });
    },
    sockets: {
        newResponse(data) {
            lesson_utils.updateResponse(data.question_id, data);
        }
    },
    components: {RubricModal}
}
</script>

<style lang="sass">
@import "~bulmaswatch/flatly/variables"
@import "@/my-colors.sass"

.teacher-view
    .apella-question
        background: $low-contrast

        &:hover
            background: $grey
            cursor: pointer

    .chart-container
        position: relative

        label
            padding: 0.5em

        svg
            margin-top: 0.5em
            position: relative
            width: 10em
            height: 1em
            border: 1px solid $grey

    .apella-responses
        border: 1px solid $grey
        border-radius: 5px

        margin: 1em
        padding: 1em

        display: grid

        &.choice, &.inline-text, &.inline-select
            grid-template-columns: repeat(auto-fill, 12em)

        &.inline-select
            .option-display
                grid-column: 1 / -1

        .student-response
            margin: 0.3em
            border: 1px solid $grey

            .name
                margin: 0.5em
                display: flex
                align-items: center
                justify-content: space-between

            &.choice
                display: flex
                align-items: stretch

                .name
                    flex-grow: 1

                .selection
                    padding: 0.5em
                    background: $grey

                    display: flex
                    align-items: center

            &.paragraph
                .answer
                    background: $grey
                    border-radius: 5px
                    margin: 0.5em
                    padding: 0.5em

            &.inline-text, &.inline-select
                .answer
                    background: $grey
                    padding: 0.5em

    .toggle-lock-btn
        &:hover
            cursor: pointer
            background: $grey

        padding: 0.75em
        width: 2.75em
</style>
