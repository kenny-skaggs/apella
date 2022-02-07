<template>
  <div>
    <div class="tile-container">
      <Tile v-for='lesson in lessons' :key='lesson.id'
            :editable='userIsAuthor' @edit='editItemClicked(lesson)'
            @click.native='itemSelected(lesson)'>
        {{ lesson.name }}
      </Tile>
      <Tile @click.native='newItemClicked' v-if='userIsAuthor'>
        <div style="text-align: center">
          <b-icon pack="fas" icon="plus-square" size="is-large"></b-icon>
        </div>
        Add Lesson
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
import AuthCheckMixin from "../mixins/AuthCheckMixin";

export default {
  name: 'LessonList',
  methods: {
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
      this.$router.push({name: 'lesson_detail', params: { lessonId: item.id }});
    }
  },
  data() {
    return {
      showEditModal: false,
      itemTemplate: { id: undefined, name: '', unit_id: this.unitId },
      currentEditing: { id: undefined, name: '' },
      lessons: [ ]
    }
  },
  created() {
    this.$http.get(`/curriculum/unit/${this.unitId}`).then((response) => {
      this.lessons = response.data['lessons'];
    });
  },
  props: ['unitId'],
  components: {
    EditItemModal, Tile
  },
  mixins: [AuthCheckMixin]
}
</script>
