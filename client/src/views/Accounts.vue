<template>
  <div>
    <div>
      <b-button @click='newUserClicked'>Add New User</b-button>
    </div>
    <p v-for='user in users' :key='user.id'>
      {{ user.username }}
    </p>
    <b-modal v-model='showUserModal'>
      <div>Edit class</div>
      <b-field label="Username">
        <b-input v-model='editingUser.username'></b-input>
      </b-field>
      <div class="buttons">
        <b-button type="is-success" @click='submitUser'>Save</b-button>
        <b-button @click='closeUserModal'>Cancel</b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  methods: {
    newUserClicked() {
      this.editingUser = {...this.userTemplate};
      this.showUserModal = true;
    },
    submitUser() {
      this.$http.post('/users', this.editingUser).then((response) => {
        this.editingUser.id = response.data.id;
        this.users.push({...this.editingUser})
      });
      this.closeUserModal();
    },
    closeUserModal() {
      this.showUserModal = false;
    }
  },
  data() {
    return {
      editingUser: { id: undefined, username: '' },
      userTemplate: { id: undefined, username: '' },
      users: [],
      showUserModal: false
    }
  },
  created() {
    this.$http.get('/users').then((response) => {
      this.users = response.data;
    });
  }
}
</script>
