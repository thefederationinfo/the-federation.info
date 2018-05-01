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
        statsUsersHalfYear {
            date
            count
        }
    }
`

export default {
    apollo: {
        statsUsersHalfYear: query,
    },
    name: "ChartUsersHalfYear",
    data() {
        return {
            statsUsersHalfYear: [],
        }
    },
    computed: {
        chartOptions() {
            return commonChartOptions
        },
        totals() {
            const data = {}
            for (const o of this.statsUsersHalfYear) {
                data[o.date] = o.count
            }
            return [{
                data,
                name: 'Active 6 months',
            }]
        },
    },
}
</script>

<style scoped>

</style>
