<template>
    <div class="columns is-gapless">
        <div class="column is-2">
            <b-button @click='addNewPage' v-if='userIsAuthor'>Add Page</b-button>
            <PageNavigation :pages='pages' @pageClicked='pageSelected' :selected-page-id='selectedPageId'
                            @deletePage='deletePage' :editable='userIsAuthor' :lesson-id='lessonId'/>
        </div>
        <div class="column" v-if='selectedPage !== undefined'>
            <LessonAuthor v-if='userIsAuthor'
                          :selected-page='selectedPage'
                          v-model='selectedPage.html'
                          @newId='(id) => this.selectedPageId = id'
            />
            <LessonTeacher v-else-if='userIsTeacher' :lesson-html='selectedPage.html' :page-id='selectedPageId'/>
            <LessonStudent v-else :lesson-html='selectedPage.html'/>
        </div>
    </div>
</template>

<script>
import PageNavigation from '../../components/LessonPageNavigation.vue';
import AuthCheckMixin from "../../mixins/AuthCheckMixin";
import LessonStudent from "./LessonStudent";
import LessonTeacher from "./LessonTeacher";
import LessonAuthor from "./LessonAuthor";
import display from "../../utils/display";

export default {
    name: 'Lesson',
    methods: {
        pageSelected(page) {
            this.selectedPageId = page.id;
        },
        addNewPage() {
            this.pages.push({
                id: undefined,
                name: '',
                lesson_id: this.lessonId,
                html: ''
            })
        },
        deletePage(pageId) {
            this.$http.delete(`/curriculum/page/${pageId}`).then(() => {
                display.removeObject(this.pages, {id: pageId}, 'id');
            });
        }
    },
    data() {
        return {
            selectedPageId: undefined,
            pages: []
        }
    },
    created() {
        this.$http.get(`/curriculum/lesson/${this.lessonId}`).then((response) => {
            this.$store.commit('setActiveLesson', this.lessonId);

            this.pages = response.data['pages'];

            if (this.selectedPageId === undefined && this.pages.length > 0) {
                this.selectedPageId = this.pages[0].id;
            }
        });
    },
    computed: {
        selectedPage() {
            return this.pages.find((page) => page.id === this.selectedPageId);
        }
    },
    props: ['lessonId'],
    components: {
        LessonAuthor,
        LessonTeacher,
        LessonStudent,
        PageNavigation,
    },
    mixins: [AuthCheckMixin]
}
</script>

<style lang="sass">
@import "~bulmaswatch/flatly/variables"

.apella-question
    border-radius: 5px
    margin: 1em
    padding: 1em

    .choice-panel
        display: flex
        width: fit-content

        .question-choice
            padding: 1em
            border-radius: 0.5em

.inline-input
    border-top-right-radius: 0  !important
    border-bottom-right-radius: 0  !important

.inline-submit
    border-top-left-radius: 0
    border-bottom-left-radius: 0
    margin-left: -5px

.short-answer-input
    width: 15em

</style>
