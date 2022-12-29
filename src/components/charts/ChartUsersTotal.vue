<script>
import gql from "graphql-tag"
import ChartMixin from "./ChartMixin"

const query = gql`
query TotalUsers($last_year: date!) {
    thefederation_stat(where: {date: {_gte: $last_year}, node_id: {_is_null: true}, platform_id: {_is_null: true}, protocol_id: {_is_null: true}}, order_by: {date: desc}) {
        date
        users_total
    }
}
`

const platformQuery = gql`
query TotalUsersByPlatform($platformId: Int!, $last_year: date!) {
    thefederation_stat(where: {date: {_gte: $last_year}, node_id: {_is_null: true}, platform_id: {_eq: $platformId}, protocol_id: {_is_null: true}}, order_by: {date: desc}) {
        date
        users_total
    }
}
`

const nodeQuery = gql`
query TotalUsersByNode($nodeId: Int!, $last_year: date!) {
    thefederation_stat(where: {date: {_gte: $last_year}, node_id: {_eq: $nodeId}, protocol_id: {_is_null: true}, platform_id: {_is_null: true}}, order_by: {date: desc}) {
        date
        users_total
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
                if (this.nodeId) {
                    return nodeQuery
                }
                return query
            },
            manual: true,
            result({data}) {
                if (data.thefederation_stat) {
                    this.stats = data.thefederation_stat.map((stat) => ({
                        date: stat.date,
                        count: stat.users_total !== null ? stat.users_total : 0,
                    }))
                }
            },
            variables() {
                const vars = {last_year: new Date(new Date().setFullYear(new Date().getFullYear() - 1))}
                if (this.platformId) {
                    return {...vars, platformId: this.platformId}
                }
                if (this.nodeId) {
                    return {...vars, nodeId: this.nodeId}
                }
                return vars
            },
        },
    },
    name: "ChartUsersTotal",
    mixins: [ChartMixin],
}
</script>
