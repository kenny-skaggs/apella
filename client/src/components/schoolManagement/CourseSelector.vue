<template>
    <b-modal v-model='showModal'>
        Select a course to make available to {{ schoolName }}
        <div class="course-list">
            <div class="course" v-for="course in sortedCourses" :key='course.id'
                @click='courseSelected(course)'
            >
                {{ course.name }}
            </div>
        </div>
        <b-button @click='closeModal'>Cancel</b-button>
    </b-modal>
</template>

<script>
import display from "../../utils/display";

export default {
    methods: {
        closeModal() {
            this.$emit('cancel');
        },
        courseSelected(course) {
            this.$emit('addCourse', course);
        }
    },
    computed: {
        sortedCourses() {
            return display.sortedObjects(this.courses, 'name');
        }
    },
    props: ['courses', 'showModal', 'schoolName']
}
</script>

<style lang="sass" scoped>
@import "~bulmaswatch/darkly/variables"

.course-list
    max-height: 70%
    overflow: scroll
    margin: 2em

.course
    display: flex
    align-items: center
    padding: 1em
    min-height: 4em
    border-bottom: 1px white solid

    &:hover
        cursor: pointer
        background: $grey-dark

</style>
