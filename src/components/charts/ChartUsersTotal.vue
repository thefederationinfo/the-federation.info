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
        statsUsersTotal {
            date
            count
        }
    }
`

export default {
    apollo: {
        statsUsersTotal: query,
    },
    name: "ChartUsersTotal",
    data() {
        return {
            statsUsersTotal: [],
        }
    },
    computed: {
        chartOptions() {
            return commonChartOptions
        },
        totals() {
            const data = {}
            for (const o of this.statsUsersTotal) {
                data[o.date] = o.count
            }
            return [{
                data,
                name: 'Total users',
            }]
        },
    },
}
</script>

<style scoped>

</style>
