<template>
    <div>
        <div v-if='school' class="school-details">
            <h1>{{ school.name }}</h1>
            <b-collapse class="panel" animation="slide" v-model='showCourses'>
                <template #trigger>
                    <div class="panel-heading" role="button" :aria-expanded='showCourses'>
                        <strong>Courses</strong>
                    </div>
                </template>
                <div class="panel-block" v-for='course in school.courses' :key='course.id'>
                    <span class="course-name">
                        {{ course.name }}
                    </span>
                    <b-button type="is-danger" icon-right="trash" icon-pack="fas" @click='removeCourse(course)' />
                </div>
                <div class="panel-block">
                    <b-button @click='showCourseSelector = true'>
                        Add Course
                    </b-button>
                </div>
            </b-collapse>
            <b-collapse class="panel" animation="slide" v-model='showTeachers'>
                <template #trigger>
                    <div class="panel-heading" role="button" :aria-expanded='showTeachers'>
                        <strong>Teachers</strong>
                    </div>
                </template>
                <div class="panel-block">
                    <b-button>Add Teacher</b-button>
                </div>
            </b-collapse>
            <CourseSelector :show-modal='showCourseSelector'
                            :courses='courses'
                            :school-name='school.name'
                            @addCourse='addCourse'
                            @cancel='showCourseSelector = false' />
        </div>
    </div>
</template>

<script>
import CourseSelector from "./CourseSelector";
import display from "../../utils/display";

export default {
    data() {
        return {
            courses: [],
            showCourses: true,
            showTeachers: true,
            showCourseSelector: false,
            school: undefined
        }
    },
    methods: {
        loadSchool() {
            this.$http.get(`/organization/school/${this.schoolId}`).then((response) => {
                this.school = response.data;
            });
            this.$http.get('/curriculum/courses').then((response) => {
                this.courses = response.data;
            });
        },
        addCourse(course) {
            this.$http.post('/organization/school-course', {
                schoolId: this.school.id,
                courseId: course.id
            }).then(() => {
                this.showCourseSelector = false;
                this.school.courses.push(course);
            });
        },
        removeCourse(course) {
            this.$http.delete(`/organization/school/${this.school.id}/course/${course.id}`, {
                schoolId: this.school.id,
                courseId: course.id
            }).then(() => {
                display.removeObject(this.school.courses, course, 'id');
            });
        }
    },
    created() {
        this.loadSchool();
    },
    watch: {
        schoolId() {
            this.loadSchool();
        }
    },
    props: ['schoolId'],
    components: {CourseSelector}
}
</script>

<style lang="sass" scoped>
.school-details .panel-block:hover
    color: inherit

.course-name
    width: 15em
</style>
