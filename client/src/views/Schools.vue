<template>
    <div class="columns is-gapless">
        <div class="column is-2">
            <b-button @click='showSchoolModal = true'>Add School</b-button>
            <div class="school-navigator">
                <div v-for='school in sortedSchools' :key='school.id'
                     :class="{'school': true, 'selected': selectedSchool !== undefined && selectedSchool.id === school.id}"
                     @click='schoolSelected(school)'
                >
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
            this.$store.commit('setIsLoading', true);
            this.$http.post('/organization/schools', schoolData).then((response) => {
                this.schools.push(response.data);
                this.showSchoolModal = false;
            }).finally(() => this.$store.commit('setIsLoading', false));
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
        this.$store.commit('setIsLoading', true)
        this.$http.get('/organization/schools').then((response) => {
            this.schools = response.data;
        }).finally(() => this.$store.commit('setIsLoading', false));
    },
    components: {SchoolModal, SchoolDetails}
}
</script>

<style lang="sass" scoped>
@import "~bulmaswatch/flatly/variables"
@import "@/my-colors.sass"

.school-navigator
    border-right: 1px $low-contrast solid

    max-height: 60vh
    overflow: scroll

.school
    display: flex
    align-items: center
    padding: 1em
    min-height: 4em
    border-bottom: 1px $low-contrast solid

    &:hover
        cursor: pointer
        background: $low-contrast

    &.selected
        background: $grey-lighter

</style>
