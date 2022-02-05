<template>
  <div>
    <div class="tile-container">
      <Tile v-for='unit in units' :key='unit.id' @edit='editItemClicked(unit)' @click.native='itemSelected(unit)'>
        {{ unit.name }}
      </Tile>
      <Tile @click.native='newItemClicked'>
        <div style="text-align: center">
          <b-icon pack="fas" icon="plus-square" size="is-large"></b-icon>
        </div>
        Add Unit
      </Tile>
    </div>
    <EditItemModal :show-modal='showEditModal' @submit='submitModal' @close='closeModal'>
      <b-field label="Name">
        <b-input v-model='currentEditing.name'></b-input>
      </b-field>
    </EditItemModal>
  </div>
</template>

<script>
import EditItemModal from "../components/curriculum/EditItemModal";
import Tile from '../components/curriculum/Tile';

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
      this.$router.push({name: 'unit_detail', params: {unitId: item.id }});
    }
  },
  data() {
    return {
      showEditModal: false,
      itemTemplate: { id: undefined, name: '', course_id: this.courseId },
      currentEditing: { id: undefined, name: '' },
      units: [ ]
    }
  },
  created() {
    this.$http.get(`/curriculum/course/${this.courseId}`).then((response) => {
      this.units = response.data['units'];
    });
  },
  props: ['courseId'],
  components: {
    EditItemModal, Tile
  }
}
</script>
