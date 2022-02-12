<template>
  <div class="columns">
    <div class="column is-3">
      <draggable :sort='false' :list='students' :group='{name: "classes", pull: "clone", put: false}'>
        <div class="student" v-for='student in students' :key='student.id'>
          {{ student.username }}
        </div>
      </draggable>
    </div>
    <div class="column">
      <b-button @click='newClassClicked'>New Class</b-button>
      <draggable v-for='cls in classList' class="class" :sort='false' :list='cls.students' group="classes" :key='cls.id'
            @change='(event) => classListChanged(event, cls)'>
        <h2>{{ cls.name }}</h2>
        <b-button class="is-small" @click='editClass(cls)'>Edit</b-button>
        <div class="student" v-for='student in cls.students' :key='student.id'>
          {{ student.username }}
        </div>
      </draggable>
    </div>
    <b-modal v-model='showEditClassModal'>
      <div>Edit class</div>
      <b-field label="Name">
        <b-input v-model='classEditing.name'></b-input>
      </b-field>
      <div class="buttons">
        <b-button type="is-success" @click='submitClass'>Save</b-button>
        <b-button @click='closeClassModal'>Cancel</b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import draggable from 'vuedraggable';

export default {
  data() {
    return {
      classTemplate: { id: undefined, name: '' },
      classEditing: { id: undefined, name: '' },
      classList: [],
      students: [],
      showEditClassModal: false
    }
  },
  created() {
    this.$http.get('/users').then((response) => {
      this.students = response.data;
    });
    this.$http.get('/organization/classes').then((response) => {
      this.classList = response.data;
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
      this.classEditing = {...cls};
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
        }
        this.closeClassModal();
      });
    },
    closeClassModal() {
      this.showEditClassModal = false;
    }
  },
  components: {draggable}
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/variables"

.student
  margin: 1em
  padding: .5em
  background: $grey

.class
  border: 1px solid $grey
  margin: 2em
  padding: 1em

</style>
