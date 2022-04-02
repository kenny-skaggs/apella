<template>
    <b-modal v-model='showModal'>
        <div class="rubric-item-row" v-for='item in rubricItems' :key='item.id'>
            <div class="description">
                {{ item.text }}
            </div>
            <b-field class="points" label="Points" horizontal>
                <b-numberinput
                    controls-position="compact"
                    controls-rounded
                    icon-pack="fas"
                />
            </b-field>
            <div class="points-total">
                out of {{ item.points }}
            </div>
        </div>
    </b-modal>
</template>

<script>
export default {
    props: ['rubricItems', 'value'],
    computed: {
        showModal: {
            get() {
                return this.value;
            },
            set(value) {
                this.$emit('input', value);
            }
        }
    }
}
</script>

<style lang="sass">
@import "~bulmaswatch/darkly/variables"

.rubric-item-row
    border-bottom: 1px solid $grey
    padding: 0.8em

    display: flex
    align-items: center

    .description
        flex-grow: 1
        margin-bottom: 0.75rem

    .points
        width: 15em

    .points-total
        margin-bottom: 0.75rem
        margin-left: 0.5rem
        width: 5em

    .is-horizontal
        align-items: center
</style>
