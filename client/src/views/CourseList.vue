<template>
    <div>
        <div class="tile-container">
            <Tile v-for='course in courses' :key='course.id'
                  header-color="#fbc212"
                  :editable='shouldViewAuthorControls' @edit='editCourse(course)'
                  @click.native='courseSelected(course, false)'
            >
                {{ course.name }}
            </Tile>
            <Tile @click.native='newCourseClicked' v-if='shouldViewAuthorControls'>
                <div style="text-align: center">
                    <b-icon pack="fas" icon="plus-square" size="is-large"></b-icon>
                </div>
                Add Course
            </Tile>
        </div>
        <template v-if='shouldViewTeachingControls && pdCourses.length > 0'>
            <hr>
            <h3>My Courses</h3>
            <div class="tile-container">
                <Tile v-for='course in pdCourses' :key='course.id'
                      header-color="#fbc212"
                      @click.native='courseSelected(course, true)'
                >
                    {{ course.name }}
                </Tile>
            </div>
        </template>

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
        courseSelected(course, is_pd_course) {
            this.$store.commit('setActiveCourse', course)
            this.$router.push({name: 'course_detail', params: {courseId: course.id}});

            if (is_pd_course) {
                this.$store.commit('setViewAsPdCourse', is_pd_course);
            }
        }
    },
    data() {
        return {
            showNewCourseModal: false,
            courseTemplate: {id: undefined, name: ''},
            currentCourseEditing: {id: undefined, name: ''},
            courses: [],
            pdCourses: []
        }
    },
    mounted() {
        this.$http.get('/curriculum/courses').then((response) => {
            this.courses = response.data;
        });
        if (this.shouldViewTeachingControls) {
            this.$http.get('/curriculum/pd-courses').then((response) => {
                this.pdCourses = response.data;
            });
        }
    },
    beforeUpdate() {
        this.$store.commit('clearCurrentCourse');
        this.$store.commit('setViewAsPdCourse', false);
    },
    components: {
        EditItemModal, Tile
    },
    mixins: [AuthCheckMixin]
}
</script>
