<template>
    <div>
        <draggable :list='units' class="tile-container" :animation='100'
                   handle=".move-handle" @change='reorderUnits' draggable=".unit-tile"
        >
            <Tile v-for='unit in units'
                  :key='unit.id'
                  class="unit-tile"
                  :editable='userIsAuthor'
                  orderable='true'
                  @edit='editItemClicked(unit)'
                  @click.native='itemSelected(unit)'
                  :item='unit'
            >
                {{ unit.name }}
                <DisplayResourceList v-if='unit.resources.length > 0' :resources='unit.resources' />
            </Tile>
            <Tile slot="footer" key="footer" @click.native='newItemClicked' v-if='userIsAuthor'>
                <div style="text-align: center">
                    <b-icon pack="fas" icon="plus-square" size="is-large"></b-icon>
                </div>
                Add Unit
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

export default {
    name: 'UnitList',
    methods: {
        newItemClicked() {
            this.currentEditing = {...this.itemTemplate};
            this.showEditModal = true;
        },
        async submitModal() {
            this.$store.commit('setIsLoading', true);

            await this.$http.post('/curriculum/units', this.currentEditing).then((response) => {
                if (this.currentEditing.id === undefined) {
                    this.currentEditing.id = response.data;
                    this.units.push({...this.currentEditing});
                } else {
                    const itemEdited = this.units.find((unit) => unit.id === this.currentEditing.id);
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
            this.$store.commit('setActiveUnit', item);
            this.$router.push({name: 'unit_detail', params: {unitId: item.id}});
        },
        reorderUnits() {

        }
    },
    data() {
        return {
            showEditModal: false,
            itemTemplate: {id: undefined, name: '', course_id: this.courseId},
            currentEditing: {id: undefined, name: '', resources: []},
            units: []
        }
    },
    created() {
        this.$http.get(`/curriculum/course/${this.courseId}`).then((response) => {
            this.units = response.data['units'];
        });
    },
    props: ['courseId'],
    beforeUpdate() {
        this.$store.commit('clearCurrentUnit');
    },
    components: {
        EditItemModal, Tile, draggable, EditResourceList, DisplayResourceList
    },
    mixins: [AuthCheckMixin]
}
</script>
