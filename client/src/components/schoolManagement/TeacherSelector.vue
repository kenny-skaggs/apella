<template>
    <b-modal v-model='showModal'>
        <div v-if='!showCreateUserForm'>
            <div>
                Search for an account to add as a teacher, or create a new account to be a teacher in {{ school.name }}
            </div>
            <b-field>
                <b-input placeholder="Search accounts by email..."
                         type="search"
                         icon-pack="fas"
                         icon="search"
                         @input='searchTextUpdated'
                />
            </b-field>
            <div v-if='isLoading' class="selection-container">
                <div class="selectable-row no-hover">
                    <b-skeleton animated />
                </div>
                <div class="selectable-row no-hover">
                    <b-skeleton animated />
                </div>
            </div>
            <div v-if='!isLoading && matchingUsers !== undefined'>
                <div v-if='matchingUsers.length === 0'>
                    No matching users found.
                </div>
                <div v-else class="selection-container">
                    <div class="selectable-row" v-for='teacher in matchingUsers' :key='teacher.id' @click='linkTeacher(teacher)'>
                        {{ teacher.first_name }} {{ teacher.last_name }} ({{ teacher.email }})
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <b-field label="First Name">
                <b-input v-model='firstName' />
            </b-field>
            <b-field label="Last Name">
                <b-input v-model='lastName' />
            </b-field>
            <b-field label="Email Address">
                <b-input v-model='email' />
            </b-field>
        </div>
        <div class="buttons">
            <b-button v-if='!showCreateUserForm' type="is-primary" @click='showCreateUserForm = true'>
                New teacher account
            </b-button>
            <b-button v-else type="is-success" @click='createTeacherAccount'>
                Save
            </b-button>
            <b-button @click='closeModal'>Cancel</b-button>
        </div>
    </b-modal>
</template>

<script>
import DebounceMixin from "../../mixins/DebounceMixin";

export default {
    data() {
        return {
            isLoading: false,
            matchingUsers: undefined,
            showCreateUserForm: false,
            firstName: '',
            lastName: '',
            email: ''
        }
    },
    methods: {
        reset() {
            this.showCreateUserForm = false;
            this.matchingUsers = undefined;
            this.firstName = '';
            this.lastName = '';
            this.email = '';
        },
        closeModal() {
            this.$emit('cancel');
            this.reset();
        },
        searchTextUpdated(searchText) {
            this.debounce('userSearch', () => {
                this.isLoading = true;
                this.$http.get(`/teacher-search/${searchText}`).then((response) => {
                    this.matchingUsers = response.data;
                }).finally(() => this.isLoading = false);
            });
        },
        createTeacherAccount() {
            this.$http.post(`/new-teacher`, {
                firstName: this.firstName,
                lastName: this.lastName,
                email: this.email,
                schoolId: this.school.id
            }).then((response) => {
                this.$emit('newTeacher', response.data);
                this.closeModal();
            });
        },
        linkTeacher(teacher) {
            this.$http.post('/organization/school-teacher', {
                schoolId: this.school.id,
                userId: teacher.id
            }).then(() => {
                this.$emit('newTeacher', teacher);
                this.closeModal();
            });
        }
    },
    props: ['showModal', 'school'],
    mixins: [DebounceMixin]
}
</script>
