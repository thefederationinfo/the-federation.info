<template>
    <section class="tile">
        <header>
            <h2>Charts</h2>
        </header>
        <div id="charts-buttons">
            <div
                :class="{selected: isSelected('nodes')}"
                class="btn-medium"
                @click="selectChart('nodes')"
            >
                Nodes
            </div>
            <div
                :class="{selected: isSelected('total_users')}"
                class="btn-medium"
                @click="selectChart('total_users')"
            >
                Total users
            </div>
        </div>
        <div>
            <ChartNodes
                v-if="isSelected('nodes')"
            />
            <ChartTotalUsers
                v-if="isSelected('total_users')"
            />
        </div>
    </section>
</template>

<script>
import ChartNodes from "./charts/ChartNodes"
import ChartTotalUsers from "./charts/ChartTotalUsers"

export default {
    name: "Charts",
    components: {ChartNodes, ChartTotalUsers},
    data() {
        return {
            activeChart: 'nodes',
        }
    },
    methods: {
        isSelected(chart) {
            return chart === this.activeChart
        },
        selectChart(chart) {
            this.activeChart = chart
        },
    },
}
</script>

<style scoped>

</style>
