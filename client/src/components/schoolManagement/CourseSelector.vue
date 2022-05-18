<template>
    <b-modal v-model='showModal'>
        Select a course to make available to {{ schoolName }}
        <div class="selection-container">
            <div class="selectable-row" v-for='course in sortedCourses' :key='course.id'
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
