<template>
    <b-modal v-model='showModal'>
        <div>New School</div>
        <b-field label="Name">
            <b-input v-model='name' />
        </b-field>
        <div class="buttons">
            <b-button type="is-success" @click='submitModal'>Save</b-button>
            <b-button @click='closeModal'>Cancel</b-button>
        </div>
    </b-modal>
</template>

<script>
export default {
    props: ['showModal'],
    data() {
        return {
            name: ''
        }
    },
    methods: {
        submitModal() {
            this.$emit('submit', {
                name: this.name
            });
            this.name = '';
        },
        closeModal() {
            this.name = '';
            this.$emit('cancel');
        }
    }
}
</script>
