<template>
    <line-chart
        :data="totals"
        :library="chartOptions"
    />
</template>

<script>
import gql from 'graphql-tag'

import commonChartOptions from "./commonChartOptions"

const query = gql`
    query {
        statsLocalPosts {
            date
            count
        }
    }
`

export default {
    apollo: {
        statsLocalPosts: query,
    },
    name: "ChartLocalPosts",
    data() {
        return {
            statsLocalPosts: [],
        }
    },
    computed: {
        chartOptions() {
            return commonChartOptions
        },
        totals() {
            const data = {}
            for (const o of this.statsLocalPosts) {
                data[o.date] = o.count
            }
            return [{
                data,
                name: 'Local posts',
            }]
        },
    },
}
</script>

<style scoped>

</style>
