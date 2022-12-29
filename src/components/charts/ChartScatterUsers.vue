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
query ScatterStats($today: date!) {
    thefederation_stat(where: {date: {_eq: $today}, node_id: {_is_null: false}, platform_id: {_is_null: true}, protocol_id: {_is_null: true}}) {
        users_monthly
        users_total
    }
}
`

const platformQuery = gql`
query ScatterStatsByPlatform($today: date!, $platformid: Int!) {
    thefederation_node(where: {platform_id: {_eq: $platformid}}) {
        thefederation_stats(where: {date: {_eq: $today}, protocol_id: {_is_null: true}, users_monthly: {_is_null: false}, users_total: {_is_null: false}}) {
            users_monthly
            users_total
        }
    }
}
`

export default {
    apollo: {
        stats: {
            query() {
                if (this.platformId) {
                    return platformQuery
                }
                return query
            },
            manual: true,
            result({data}) {
                const stats = []
                if (this.platformId) {
                    for (const o of data.thefederation_node) {
                        const stat = o.thefederation_stats[0]
                        if (stat) {
                            stats.push([stat.users_total, stat.users_monthly])
                        }
                    }
                } else {
                    for (const o of data.thefederation_stat) {
                        stats.push([o.users_total, o.users_monthly])
                    }
                }
                this.stats = stats
            },
            variables() {
                const today = {today: new Date()}
                if (this.platformId) {
                    return {...today, platformid: this.platformId}
                }
                return today
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
