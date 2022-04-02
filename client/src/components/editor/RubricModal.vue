<template>
    <b-modal v-model='showModal' v-if='rubricItems'>
        <b-field v-for='item in rubricItems' :key='item.id' grouped>
            <b-field label="Text">
                <b-input v-model='item.text'/>
            </b-field>
            <b-field label="Points">
                <b-numberinput
                    v-model='item.points'
                    controls-position="compact"
                    controls-alignment="right"
                    icon-pack="fas"
                />
            </b-field>
            <b-field label="Delete">
                <b-button icon-pack="fas" icon-left="trash" type="danger" @click='removeItem(item)' />
            </b-field>
        </b-field>
        <div class="buttons">
            <b-button @click='addItem' type="is-primary">Add Item</b-button>
            <b-button @click='save' type="is-success">Save</b-button>
        </div>
    </b-modal>
</template>

<script>
export default  {
    props: ['showModal', 'rubricItems'],
    data() {
        return {
            temp_item_id: 0
        };
    },
    methods: {
        addItem() {
            this.rubricItems.push({id: `temp${this.temp_item_id++}`, 'text': ''})
        },
        removeItem(removedItem) {
            const index = this.rubricItems.findIndex((item) => item.id == removedItem.id);
            this.rubricItems.splice(index, 1);
        },
        save() {
            this.$emit('saveRubric')
        }
    }
}
</script>
