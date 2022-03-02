<template>
  <b-select rounded v-model='selectedClassId'>
    <option v-for='cls in classes' :value='cls.id' :key='cls.id'>
      {{ cls.name }}
    </option>
  </b-select>
</template>

<script>
export default {
  data() {
    return {
      classes: []
    }
  },
  created() {
    this.$http.get('/organization/classes').then((response) => {
      this.classes = response.data;

      if (this.$store.state.selectedClassId === undefined && this.classes.length > 0) {
        this.setSelectedClass(this.classes[0].id);
      }
    });
  },
  methods: {
    setSelectedClass(classId) {
      this.$store.commit('setSelectedClass', classId);
    }
  },
  computed: {
    selectedClassId: {
      get() {
        return this.$store.state.selectedClassId;
      },
      set(classId) {
        this.setSelectedClass(classId);
      }
    }
  }
}
</script>
