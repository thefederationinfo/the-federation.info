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
        statsLocalComments {
            date
            count
        }
    }
`

export default {
    apollo: {
        statsLocalComments: query,
    },
    name: "ChartLocalComments",
    data() {
        return {
            statsLocalComments: [],
        }
    },
    computed: {
        chartOptions() {
            return commonChartOptions
        },
        totals() {
            const data = {}
            for (const o of this.statsLocalComments) {
                data[o.date] = o.count
            }
            return [{
                data,
                name: 'Local comments',
            }]
        },
    },
}
</script>

<style scoped>

</style>
