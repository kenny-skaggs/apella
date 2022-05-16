<template>
    <div class="columns is-gapless">
        <div class="column is-2">
            <b-button @click='showSchoolModal = true'>Add School</b-button>
            <div class="school-navigator">
                <div v-for='school in sortedSchools' :key='school.id' class="school" @click='schoolSelected(school)'>
                    {{ school.name }}
                </div>
            </div>
        </div>
        <div class="column">
            <SchoolDetails v-if='selectedSchool' :school-id='selectedSchool.id' />
        </div>
        <SchoolModal :show-modal='showSchoolModal' @submit='submitSchoolModal' @cancel='cancelSchoolModal' />
    </div>
</template>

<script>
import SchoolModal from "../components/schoolManagement/SchoolModal";
import SchoolDetails from "../components/schoolManagement/SchoolDetails";
import display from "../utils/display";

export default {
    data() {
        return {
            schools: [],
            showSchoolModal: false,
            selectedSchool: undefined,
            showCourses: false
        };
    },
    methods: {
        submitSchoolModal(schoolData) {
            this.$http.post('/organization/schools', schoolData).then((response) => {
                this.schools.push(response.data);
                this.showSchoolModal = false;
            });
        },
        cancelSchoolModal() {
            this.showSchoolModal = false;
        },
        schoolSelected(school) {
            this.selectedSchool = school;
        }
    },
    computed:{
        sortedSchools() {
            return display.sortedObjects(this.schools, 'name');
        }
    },
    mounted() {
        this.$http.get('/organization/schools').then((response) => {
            this.schools = response.data;
        });
    },
    components: {SchoolModal, SchoolDetails}
}
</script>

<style lang="sass" scoped>
@import "~bulmaswatch/darkly/variables"

.school-navigator
    border-right: 1px white solid

.school
    display: flex
    align-items: center
    padding: 1em
    min-height: 4em
    border-bottom: 1px white solid

    &:hover
        cursor: pointer
        background: $grey-dark

    &.selected
        background: $grey

</style>
