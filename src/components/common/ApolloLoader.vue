<template>
    <div>
        <div v-if="loading">
            <div class="spinner">
                <Spinner color="#dddddd" />
            </div>
        </div>
        <div v-else>
            <slot />
        </div>
    </div>
</template>

<script>
import Spinner from 'vue-spinner-component/src/Spinner'

export default {
    name: "ApolloLoader",
    components: {Spinner},
    props: {
        loading: {
            type: Boolean,
            default: false,
        },
    },
}
</script>

<style scoped>
    .spinner {
        display: flex;
        justify-content: center;
    }
</style>
