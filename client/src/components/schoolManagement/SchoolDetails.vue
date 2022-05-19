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
                    <span class="detail-item">
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
                <div class="panel-block" v-for='teacher in school.teachers' :key='teacher.id'>
                    <span class="detail-item">
                        {{ teacher.first_name }} {{ teacher.last_name }} ({{ teacher.email }})
                    </span>
                    <b-button type="is-danger" icon-right="trash" icon-pack="fas" @click='removeTeacher(teacher)' />
                </div>
                <div class="panel-block">
                    <b-button @click='showTeacherSelector = true'>Add Teacher</b-button>
                </div>
            </b-collapse>
            <CourseSelector :show-modal='showCourseSelector'
                            :courses='availableCourses'
                            :school-name='school.name'
                            @addCourse='addCourse'
                            @cancel='showCourseSelector = false' />
            <TeacherSelector :show-modal='showTeacherSelector'
                             :school='school'
                             @newTeacher='addTeacher'
                             @cancel='showTeacherSelector = false'
            />
        </div>
    </div>
</template>

<script>
import CourseSelector from "./CourseSelector";
import TeacherSelector from "./TeacherSelector";
import display from "../../utils/display";

export default {
    data() {
        return {
            availableCourses: [],
            showCourses: true,
            showTeachers: true,
            showCourseSelector: false,
            showTeacherSelector: false,
            school: undefined
        }
    },
    methods: {
        loadSchool() {
            this.$http.get(`/organization/school/${this.schoolId}`).then((response) => {
                this.school = response.data;
            });
        },
        loadAvailableCourses() {
            this.$http.get('/curriculum/courses').then((response) => {
                this.availableCourses = response.data;
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
            this.$http.delete(`/organization/school/${this.school.id}/course/${course.id}`).then(() => {
                display.removeObject(this.school.courses, course, 'id');
            });
        },
        addTeacher(teacher) {
            this.school.teachers.push(teacher);
        },
        removeTeacher(teacher) {
            this.$http.delete(`/organization/school/${this.school.id}/teacher/${teacher.id}`).then(() => {
                display.removeObject(this.school.teachers, teacher, 'id');
            })
        }
    },
    created() {
        this.loadSchool();
        this.loadAvailableCourses();
    },
    watch: {
        schoolId() {
            this.loadSchool();
        }
    },
    props: ['schoolId'],
    components: {CourseSelector, TeacherSelector}
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/variables"

.school-details .panel-block:hover
    color: inherit

.detail-item
    width: 25em

</style>
