<template>
    <div class="columns">
        <div class="column is-3">
            <b-button @click='showStudentModal = true'>New Student</b-button>
            <draggable :sort='false' :list='students' :group='{name: "classes", pull: "clone", put: false}'>
                <div class="student" v-for='student in students' :key='student.id'>
                    <span>{{ student.first_name }} {{ student.last_name }} ({{ student.email || student.username }})</span>
                    <b-icon pack="fas" icon="edit" class="edit-btn" @click.native='editUser(student)' />
                </div>
            </draggable>
        </div>
        <div class="column">
            <b-button @click='newClassClicked'>New Class</b-button>
            <draggable v-for='cls in classList' class="class" :sort='false' :list='cls.students' group="classes"
                       :key='cls.id'
                       @change='(event) => classListChanged(event, cls)'>
                <h2>{{ cls.name }}</h2>
                <div>
                    Courses: {{ courseListDisplay(cls.course_list) }}
                </div>
                <b-button class="is-small" @click='editClass(cls)'>Edit</b-button>
                <div class="student" v-for='student in cls.students' :key='student.id'>
                    {{ student.first_name }} {{ student.last_name }} ({{ student.email }})
                </div>
            </draggable>
        </div>
        <b-modal v-model='showStudentModal'>
            <div>New Student</div>
            <b-field label="First Name">
                <b-input v-model='currentStudent.first_name'></b-input>
            </b-field>
            <b-field label="Last Name">
                <b-input v-model='currentStudent.last_name'></b-input>
            </b-field>
            <b-field label="Google Sign-In">
                <b-input v-model='currentStudent.email'></b-input>
            </b-field>
            <b-field label="Username">
                <b-input v-model='currentStudent.username'></b-input>
            </b-field>
            <b-field label="Password">
                <b-input v-model='currentStudent.password'
                         placeholder='Type here to change password'
                         type='password'
                         autocomplete='new-password'
                ></b-input>
            </b-field>
            <div class="buttons">
                <b-button type="is-success" @click='submitStudent'>Save</b-button>
                <b-button @click='closeStudentModal'>Cancel</b-button>
            </div>
        </b-modal>
        <b-modal v-model='showEditClassModal'>
            <div>Edit class</div>
            <b-field label="Name">
                <b-input v-model='classEditing.name'></b-input>
            </b-field>
            Courses Available:
            <div class="selection-container">
                <div :class="{'selectable-row': true, 'is-selected': isCourseSelected(course)}"
                     @click='toggleCourse(course)'
                     v-for='course in courseList'
                     :key='course.id'
                >
                    {{ course.name }}
                </div>
            </div>
            <div class="buttons">
                <b-button type="is-success" @click='submitClass'>Save</b-button>
                <b-button @click='closeClassModal'>Cancel</b-button>
            </div>
        </b-modal>
    </div>
</template>

<script>
import draggable from 'vuedraggable';
import display from "../utils/display";
import { cloneDeep } from 'lodash';

export default {
    data() {
        return {
            classTemplate: {id: undefined, name: '', course_list: []},
            classEditing: {id: undefined, name: '', course_list: []},
            classList: [],
            students: [],
            showEditClassModal: false,
            courseList: [],
            showStudentModal: false,
            currentStudent: this.getStudentDataTemplate()
        }
    },
    created() {
        this.$http.get('/users').then((response) => {
            this.students = response.data;
        });
        this.$http.get('/organization/classes').then((response) => {
            this.classList = response.data;
        });
        this.$http.get('/curriculum/courses').then((response) => {
            this.courseList = response.data;
        });
    },
    methods: {
        classListChanged({added}, cls) {
            this.$http.post(`/organization/class/${cls.id}/student/${added.element.id}`)
        },
        newClassClicked() {
            this.classEditing = {...this.classTemplate};
            this.showEditClassModal = true;
        },
        editClass(cls) {
            this.classEditing = cloneDeep(cls);
            this.showEditClassModal = true;
        },
        submitClass() {
            const editId = this.classEditing.id;
            const url = editId === undefined ? '/organization/classes' : `/organization/class/${editId}`
            this.$http.post(url, this.classEditing).then((response) => {
                if (editId === undefined) {
                    this.classEditing.id = response.data.id
                    this.classList.push({...this.classEditing});
                } else {
                    const editedClass = this.classList.find((cls) => cls.id === this.classEditing.id);
                    editedClass.name = this.classEditing.name;
                    editedClass.course_list = this.classEditing.course_list;
                }
                this.closeClassModal();
            });
        },
        submitStudent() {
            this.$http.post('/users', this.currentStudent).then((response) => {
                if (this.currentStudent.id === undefined) {
                    this.currentStudent.id = response.data.id;
                    this.students.push(...this.currentStudent);
                } else {
                    const editedStudent = this.students.find((student) => student.id === this.currentStudent.id);
                    Object.assign(editedStudent, this.currentStudent);
                }
                this.currentStudent = this.getStudentDataTemplate();
                this.showStudentModal = false;
            });
        },
        closeClassModal() {
            this.showEditClassModal = false;
        },
        closeStudentModal() {
            this.showStudentModal = false;
            this.currentStudent = this.getStudentDataTemplate();
        },
        editUser(student) {
            this.currentStudent = {...student};
            this.showStudentModal = true;
        },
        getStudentDataTemplate() {
            return {
                id: undefined,
                first_name: '',
                last_name: '',
                email: '',
                username: '',
                password: ''
            }
        },
        courseListDisplay(course_list) {
            return course_list.map((course) => course.name).join(', ');
        },
        toggleCourse(course) {
            if (this.isCourseSelected(course)) {
                display.removeObject(this.classEditing.course_list, course, 'id');
            } else {
                this.classEditing.course_list.push(course);
            }
        },
        isCourseSelected(course) {
            const index = this.classEditing.course_list.findIndex((item) => item.id === course.id);
            return index >= 0;
        }
    },
    components: {draggable}
}
</script>

<style lang="sass" scoped>
@import "~bulmaswatch/flatly/variables"

.student
    margin: 1em
    padding: 0.75em
    background: $grey
    display: flex
    justify-content: space-between
    align-items: center

    .edit-btn:hover
        cursor: pointer

.class
    border: 1px solid $grey
    margin: 2em
    padding: 1em

.is-selected
    background: $grey !important

</style>
