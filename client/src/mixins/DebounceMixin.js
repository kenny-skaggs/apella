export default {
    data() {
        return {
            debounceTracker: {}
        }
    },
    methods: {
        debounce(key, func) {
            let currentTimeout = this.debounceTracker[key];
            if (currentTimeout !== undefined) {
                clearTimeout(currentTimeout);
            }
            this.debounceTracker[key] = setTimeout(func, 300);
        }
    }
}