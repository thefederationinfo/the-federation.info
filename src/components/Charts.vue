<template>
    <section class="tile">
        <header>
            <h2>Charts</h2>
        </header>
        <div>
            <ChartNodes />
        </div>

    </section>
</template>

<script>
import ChartNodes from "./charts/ChartNodes"

export default {
    name: "Charts",
    components: {ChartNodes},
}
</script>

<style scoped>
    /*.chart-container {*/
        /*min-height: 300px;*/
    /*}*/
</style>
