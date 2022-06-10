<template>
    <div>
        <draggable :list='lessons' class="tile-container" :animation='100'
                   handle=".move-handle" @change='reorderLessons' draggable=".lesson-tile"
        >
            <Tile v-for='lesson in lessons'
                  :key='lesson.id'
                  header-color="#EC1C2d"
                  class="lesson-tile"
                  :editable='userIsAuthor'
                  orderable='true'
                  @edit='editItemClicked(lesson)'
                  @click.native='itemSelected(lesson)'
                  :item='lesson'
            >
                {{ lesson.name }}
                <DisplayResourceList v-if='lesson.resources.length > 0' :resources='lesson.resources' />
                <template v-if='userIsTeacher' v-slot:extras>
                    <div>
                        <b-button size="is-small" @click.stop='toggleLessonVisibility(lesson)'>
                            {{ isLessonVisible(lesson) ? 'Hide' : 'Show' }} lesson
                        </b-button>
                    </div>
                </template>
            </Tile>
            <Tile slot="footer" key="footer" @click.native='newItemClicked' v-if='userIsAuthor'>
                <div style="text-align: center">
                    <b-icon pack="fas" icon="plus-square" size="is-large"></b-icon>
                </div>
                Add Lesson
            </Tile>
        </draggable>
        <EditItemModal :show-modal='showEditModal' @submit='submitModal' @close='closeModal'>
            <b-field label="Name">
                <b-input v-model='currentEditing.name'></b-input>
            </b-field>
            <hr>
            <EditResourceList :resource-list='currentEditing.resources' />
            <hr>
        </EditItemModal>
    </div>
</template>

<script>
import draggable from "vuedraggable";

import EditItemModal from "../components/curriculum/EditItemModal";
import Tile from '../components/curriculum/Tile';
import AuthCheckMixin from "../mixins/AuthCheckMixin";
import EditResourceList from "../components/curriculum/EditResourceList";
import DisplayResourceList from "../components/curriculum/DisplayResourceList";
import display from "../utils/display";

export default {
    name: 'LessonList',
    methods: {
        reorderLessons() {
            const ordered_lesson_ids = this.lessons.map((lesson) => lesson.id);
            this.$http.post(`/curriculum/unit/order/${this.unitId}`, {lessonIds: ordered_lesson_ids});
        },
        newItemClicked() {
            this.currentEditing = {...this.itemTemplate};
            this.showEditModal = true;
        },
        async submitModal() {
            this.$store.commit('setIsLoading', true);

            await this.$http.post('/curriculum/lessons', this.currentEditing).then((response) => {
                if (this.currentEditing.id === undefined) {
                    this.currentEditing.id = response.data;
                    this.lessons.push({...this.currentEditing});
                } else {
                    const itemEdited = this.lessons.find((lesson) => lesson.id === this.currentEditing.id);
                    Object.assign(itemEdited, this.currentEditing);
                }
                this.closeModal();
            }).finally(() => this.$store.commit('setIsLoading', false));
        },
        closeModal() {
            this.showEditModal = false;
        },
        editItemClicked(item) {
            this.currentEditing = {...item};
            this.showEditModal = true;
        },
        itemSelected(item) {
            this.$store.commit('setActiveLesson', item);
            this.$router.push({name: 'lesson_detail', params: {lessonId: item.id}});
        },
        toggleLessonVisibility(lesson) {
            const index = this.visibleLessonIds.findIndex((visible_id) => visible_id === lesson.id);
            if (index >= 0) {
                this.visibleLessonIds.splice(index, 1);
            } else {
                this.visibleLessonIds.push(lesson.id);
            }
        },
        isLessonVisible({ id }) {
            const index = this.visibleLessonIds.findIndex((visible_id) => visible_id === id);
            return index >= 0;
        }
    },
    data() {
        return {
            showEditModal: false,
            itemTemplate: {id: undefined, name: '', unit_id: this.unitId, resources: []},
            currentEditing: {id: undefined, name: '', resources: []},
            lessons: [],
            visibleLessonIds: []
        }
    },
    created() {
        this.$http.get(`/curriculum/unit/${this.unitId}`).then((response) => {
            this.lessons = response.data['lessons'];
        });
    },
    props: ['unitId'],
    beforeUpdate() {
        this.$store.commit('clearCurrentLesson');
    },
    components: {
        EditItemModal, Tile, draggable, EditResourceList, DisplayResourceList
    },
    mixins: [AuthCheckMixin]
}
</script>
