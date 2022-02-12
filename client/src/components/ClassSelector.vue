<template>
  <b-select rounded>
    <option v-for='cls in classes' :value='cls.id' :key='cls.id'>{{ cls.name }}></option>
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
    });
  }
}
</script>
