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
// Platform icons live in /static/images. The DB icon field is ignored;
// the file is derived from the platform name, lowercased with spaces
// replaced by dashes. Preferred lookup order: <slug>.svg, then <slug>.png.
// If neither exists the image is not rendered at all.
export default {
    name: "PlatformIcon",
    props: {
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
        slug() {
            return this.name.toLowerCase().split(' ').join('-')
        },
        candidates() {
            return [
                `/static/images/${this.slug}.svg`,
                `/static/images/${this.slug}.png`,
            ]
        },
        exhausted() {
            return this.current >= this.candidates.length
        },
    },
    watch: {
        name() {
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
