<template>
    <div>
        <b-field grouped v-for='resource in resourceList' :key='resource.id'>
            <b-field label="Name">
                <b-input v-model='resource.name' />
            </b-field>
            <b-field label="Link">
                <b-input v-model='resource.link' />
            </b-field>
        </b-field>
        <b-button @click='newResource'>Add Resource</b-button>
    </div>
</template>

<script>
import { debounce } from 'lodash';

export default {
    name: 'ResourceList',
    data() {
        return {
            tempResourceCount: 0,
            timeoutTracker: {}
        }
    },
    methods: {
        newResource() {
            const newResource = {
                id: this.getNextTempResourceId(),
                name: '',
                link: ''
            };
            this.resourceList.push(newResource);
        },
        getNextTempResourceId() {
            this.tempResourceCount += 1;
            return `temp${this.tempResourceCount}`;
        }
    },
    props: ['resourceList']
}
</script>
