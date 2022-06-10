<template>
    <div class="curriculum-tile">
        <div v-if='headerColor' :style='{ "background-color": headerColor}' class='header'></div>
        <div class="edit-panel" v-if='editable'>
            <div @click.stop=''>
                <b-dropdown aria-role="list">
                    <template #trigger>
                        <b-icon pack="fas" icon="ellipsis-v"/>
                    </template>

                    <b-dropdown-item aria-role="listitem" @click="editClicked">Edit</b-dropdown-item>
                    <b-dropdown-item aria-role="listitem">Delete</b-dropdown-item>
                </b-dropdown>
            </div>

            <b-icon v-if='orderable' pack="fas" icon="grip-lines" class="move-handle"/>
        </div>
        <div class="tile-body">
            <slot></slot>
            <template v-if='item'>
                <div v-for='resource in item.resource' :key='resource.value'>
                    <a :href='resource.link'>{{ resource.name }}</a>
                </div>
            </template>
            <slot name="extras" />
        </div>
    </div>
</template>

<script>
export default {
    name: 'Tile',
    methods: {
        editClicked() {
            this.$emit('edit');
        }
    },
    props: ['editable', 'orderable', 'item', 'headerColor']
}
</script>

<style lang="sass">
@import "../../../node_modules/bulmaswatch/flatly/variables"
.curriculum-tile
    position: relative

    width: 15em
    min-height: 8em
    margin: 2em
    border-radius: 1em

    padding-top: 4em
    padding-bottom: 2em

    border: 1px solid $grey

    display: flex
    flex-direction: column
    align-items: center
    justify-content: center

    &:hover
        background-color: $grey-lighter
        cursor: pointer
        color: #333

    .header
        position: absolute
        left: 0
        right: 0
        top: 0
        height: 3em
        border-top-left-radius: 1em
        border-top-right-radius: 1em

.edit-panel
    position: absolute
    right: 1em
    top: 1em
    left: 1em

    display: flex
    flex-direction: row-reverse
    justify-content: space-between
    align-items: center

    .move-handle
        cursor: move

</style>
