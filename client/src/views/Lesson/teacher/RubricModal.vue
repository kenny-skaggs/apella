<template>
    <b-modal class="rubric-modal" v-model='showModal'>
        <div class="tile is-ancestor">
            <div class="tile is-3 is-parent is-vertical is-justify-content-flex-start">
                <div class="tile is-child student-list">
                    <div class="student"
                         v-for='student in studentMap'
                         :key='student.id'
                         :class='{
                             "disabled": !studentHasResponse(student),
                             "selected": selectedStudentId === student.id
                         }'
                         @click='studentSelected(student)'
                    >
                        {{ student.username }}
                        <em v-if='!studentHasResponse(student)'> - no submission</em>
                    </div>
                </div>
            </div>
            <div class="tile is-vertical is-parent">
                <div class="tile is-child">
                    <iframe :src='currentResponse.text' title="student submission"></iframe>
                    <a :href='currentResponse.text' target="_blank">Open in new tab</a>
                </div>
                <div class="is-parent is-vertical grades-list">
                    <div class="tile is-child rubric-item-row" v-for='item in rubricItems' :key='item.id'>
                        <div class="description">
                            {{ item.text }}
                        </div>
                        <b-field class="points" label="Points" horizontal>
                            <b-numberinput
                                controls-position="compact"
                                controls-rounded
                                icon-pack="fas"
                                :value='getGradeFor(item.id)'
                                @input='value => rubricItemGraded(value, item.id)'
                            />
                        </b-field>
                        <div class="points-total">
                            out of {{ item.points }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </b-modal>
</template>

<script>
import _ from 'underscore';
import DebounceMixin from "../../../mixins/DebounceMixin";

export default {
    props: ['rubricItems', 'value', 'responseMap', 'studentMap'],
    data() {
        return {
            selectedStudentId: undefined
        }
    },
    computed: {
        showModal: {
            get() {
                return this.value;
            },
            set(value) {
                this.$emit('input', value);
            }
        },
        currentResponse() {
            if (this.selectedStudentId !== undefined) {
                return this.responseMap.get_response(this.selectedStudentId);
            } else {
                return {
                    text: '',
                    rubric_grades: []
                }
            }
        },
        getGradeFor() {
            return (itemId) => {
                let existingGrade = this.currentResponse.rubric_grades.find(grade => grade.rubric_item_id === itemId);
                if (existingGrade === undefined) {
                    return undefined;
                } else {
                    return existingGrade.grade;
                }
            }
        }
    },
    methods:{
        studentHasResponse(student) {
            return this.responseMap !== undefined && student.id in this.responseMap.map;
        },
        studentSelected(student) {
            this.selectedStudentId = student.id;
        },
        rubricItemGraded(newGradeValue, rubricItemId) {
            let responseId = this.currentResponse.id;
            let existingGrade = this.currentResponse.rubric_grades.find(grade => grade.rubric_item_id === rubricItemId);
            if (existingGrade === undefined) {
                existingGrade = { rubric_item_id: rubricItemId }
                this.currentResponse.rubric_grades.push(existingGrade);
            }
            existingGrade.grade = newGradeValue;

            this.debounce([responseId, rubricItemId], () => {
                this.$http.post(
                    `/responses/answer/${responseId}/grade-rubric-item/${rubricItemId}`,
                    { grade: newGradeValue }
                )
            });
        },
    },
    watch:{
        responseMap() {
            this.selectedStudentId = undefined;
        }
    },
    mixins: [DebounceMixin]
}
</script>

<style lang="sass">
@import "~bulmaswatch/flatly/variables"
@import "@/my-colors.sass"

.rubric-item-row
    border-bottom: 1px solid $grey
    padding: 0.8em

    display: flex
    align-items: center

    .description
        flex-grow: 1
        margin-bottom: 0.75rem

    .points
        width: 15em

    .points-total
        margin-bottom: 0.75rem
        margin-left: 0.5rem
        width: 5em

    .is-horizontal
        align-items: center

.rubric-modal
    iframe
        width: 100%
        height: 15rem

    .grades-list
        height: calc(100vh - 23rem)
        overflow-y: scroll

    .student-list
        height: 100vh
        overflow-y: scroll

        .student
            padding: 1rem

            &:hover:not(.disabled):not(.selected)
                background: $low-contrast
                cursor: pointer

            &.disabled
                color: $grey

            &.selected
                background: $grey
</style>
