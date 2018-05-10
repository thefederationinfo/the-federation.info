<template>
    <div>
        <div v-if="$apollo.loading">
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
}
</script>

<style scoped>
    .spinner {
        display: flex;
        justify-content: center;
    }
</style>
