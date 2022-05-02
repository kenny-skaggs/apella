<template>
    <div @click.stop='' style="width: fit-content">
        <b-dropdown aria-role="list">
            <template #trigger>
                <b-button
                    size="is-small"
                    class="resources-btn"
                >
                    Resources
                </b-button>
            </template>

            <b-dropdown-item v-for='resource in resources' :key='resource.id' aria-role="listitem">
                <a :href='resource.link' target="_blank">{{ resource.name }}</a>
            </b-dropdown-item>
        </b-dropdown>
    </div>
</template>

<script>
export default {
    props: ['resources']
}
</script>

<style lang="sass" scoped>
.resources-btn
    margin-top: 1em
</style>
