<script>
import gql from "graphql-tag"
import ChartMixin from "./ChartMixin"

const query = gql`
query LocalPosts($last_year: date!) {
    thefederation_stat(where: {date: {_gte: $last_year}, node_id: {_is_null: true}, platform_id: {_is_null: true}, protocol_id: {_is_null: true}}, order_by: {date: desc}) {
        date
        local_posts
    }
}
`

const platformQuery = gql`
query LocalPostsByPlatform($platformId: Int!, $last_year: date!) {
    thefederation_stat(where: {date: {_gte: $last_year}, node_id: {_is_null: true}, platform_id: {_eq: $platformId}, protocol_id: {_is_null: true}}, order_by: {date: desc}) {
        date
        local_posts
    }
}
`

const nodeQuery = gql`
query LocalPostsByNode($nodeId: Int!, $last_year: date!) {
    thefederation_stat(where: {date: {_gte: $last_year}, node_id: {_eq: $nodeId}, protocol_id: {_is_null: true}, platform_id: {_is_null: true}}, order_by: {date: desc}) {
        date
        local_posts
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
                        count: stat.local_posts,
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
    name: "ChartLocalPosts",
    mixins: [ChartMixin],
}
</script>
