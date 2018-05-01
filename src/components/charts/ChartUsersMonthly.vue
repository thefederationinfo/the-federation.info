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
        statsUsersMonthly {
            date
            count
        }
    }
`

export default {
    apollo: {
        statsUsersMonthly: query,
    },
    name: "ChartUsersMonthly",
    data() {
        return {
            statsUsersMonthly: [],
        }
    },
    computed: {
        chartOptions() {
            return commonChartOptions
        },
        totals() {
            const data = {}
            for (const o of this.statsUsersMonthly) {
                data[o.date] = o.count
            }
            return [{
                data,
                name: 'Active last month',
            }]
        },
    },
}
</script>

<style scoped>

</style>
