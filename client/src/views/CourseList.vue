<template>
    <div>
        <div class="tile-container">
            <Tile v-for='course in courses' :key='course.id'
                  header-color="#fbc212"
                  :editable='userIsAuthor' @edit='editCourse(course)'
                  @click.native='courseSelected(course)'
            >
                {{ course.name }}
            </Tile>
            <Tile @click.native='newCourseClicked' v-if='userIsAuthor'>
                <div style="text-align: center">
                    <b-icon pack="fas" icon="plus-square" size="is-large"></b-icon>
                </div>
                Add Course
            </Tile>
        </div>
        <EditItemModal :show-modal='showNewCourseModal' @submit='submitModal' @close='closeModal'>
            <b-field label="Name">
                <b-input v-model='currentCourseEditing.name'></b-input>
            </b-field>
        </EditItemModal>
    </div>
</template>

<script>
import EditItemModal from "../components/curriculum/EditItemModal";
import Tile from '../components/curriculum/Tile';
import AuthCheckMixin from "../mixins/AuthCheckMixin";
import toast from "../utils/toasts";

export default {
    name: 'CourseList',
    methods: {
        newCourseClicked() {
            this.currentCourseEditing = {...this.courseTemplate};
            this.showNewCourseModal = true;
        },
        async submitModal() {
            this.$store.commit('setIsLoading', true);

            await this.$http.post('/curriculum/courses', this.currentCourseEditing).then((response) => {
                if (this.currentCourseEditing.id === undefined) {
                    this.currentCourseEditing.id = response.data;
                    this.courses.push({...this.currentCourseEditing});
                } else {
                    const courseEdited = this.courses.find((course) => course.id === this.currentCourseEditing.id);
                    Object.assign(courseEdited, this.currentCourseEditing);
                }
                this.closeModal();
            }).finally(() => this.$store.commit('setIsLoading', false));
        },
        closeModal() {
            this.showNewCourseModal = false;
        },
        editCourse(course) {
            this.currentCourseEditing = {...course};
            this.showNewCourseModal = true;
        },
        courseSelected(course) {
            this.$store.commit('setActiveCourse', course)
            this.$router.push({name: 'course_detail', params: {courseId: course.id}});
        }
    },
    data() {
        return {
            showNewCourseModal: false,
            courseTemplate: {id: undefined, name: ''},
            currentCourseEditing: {id: undefined, name: ''},
            courses: []
        }
    },
    mounted() {
        this.$http.get('/curriculum/courses').then((response) => {
            this.courses = response.data;
        });
    },
    beforeUpdate() {
        this.$store.commit('clearCurrentCourse');
    },
    components: {
        EditItemModal, Tile
    },
    mixins: [AuthCheckMixin]
}
</script>
