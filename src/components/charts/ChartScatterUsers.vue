<template>
    <scatter-chart
        :data="stats"
        xtitle="Total users"
        ytitle="Monthly users"
    />
</template>

<script>
import gql from 'graphql-tag'

import ChartMixin from "./ChartMixin"

const query = gql`
    query ScatterStats($type: String!, $value: String!) {
        statsNodes(itemType: $type, value: $value) {
            usersTotal
            usersMonthly
        }
    }
`

export default {
    apollo: {
        stats: {
            query,
            manual: true,
            result({data}) {
                const stats = []
                for (const o of data.statsNodes) {
                    stats.push([o.usersTotal, o.usersMonthly])
                }
                this.stats = stats
            },
            variables() {
                return {
                    type: this.type,
                    value: this.item,
                }
            },
        },
    },
    name: "ChartScatterUsers",
    mixins: [ChartMixin],
    data() {
        return {
            stats: [],
        }
    },
}
</script>
