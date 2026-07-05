<template>
    <img
        v-if="!exhausted"
        :alt="name"
        :title="name"
        :src="candidates[current]"
        class="platform-icon"
        @error="onError"
    >
</template>

<script>
// Platform icons live in /static/images. Preferred lookup order: <icon>.svg, then <icon>.png
// If none of them exists the image is not rendered at all.
export default {
    name: "PlatformIcon",
    props: {
        icon: {
            type: String,
            default: "",
        },
        name: {
            type: String,
            default: "",
        },
    },
    data() {
        return {
            current: 0,
        }
    },
    computed: {
        candidates() {
            return [
                `/static/images/${this.icon}.svg`,
                `/static/images/${this.icon}.png`,
            ]
        },
        exhausted() {
            return this.current >= this.candidates.length
        },
    },
    watch: {
        icon() {
            this.current = 0
        },
    },
    methods: {
        onError() {
            this.current += 1
        },
    },
}
</script>

<style scoped>
    .platform-icon {
        width: 1em;
        height: 1em;
        object-fit: contain;
        vertical-align: middle;
    }
</style>
