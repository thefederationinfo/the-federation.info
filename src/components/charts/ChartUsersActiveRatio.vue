<script>
import gql from "graphql-tag"
import ChartMixin from "./ChartMixin"

const query = gql`
query ActiveUsersRatio {
    active_users_ratio(order_by: {date: desc}) {
        count
        date
    }
}
`

const platformQuery = gql`
query ActiveUsersRatioByPlatform($platformId: Int!) {
    active_users_ratio_by_platform(args: {platformid: $platformId}, order_by: {date: desc}) {
        count
        date
    }
}
`

const nodeQuery = gql`
query ActiveUsersRatioByNode($nodeId: Int!) {
    active_users_ratio_by_node(args: {nodeid: $nodeId}, order_by: {date: desc}) {
        count
        date
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
                if (this.platformId) {
                    this.stats = data.active_users_ratio_by_platform
                } else if (this.nodeId) {
                    this.stats = data.active_users_ratio_by_node
                } else {
                    this.stats = data.active_users_ratio
                }
            },
            variables() {
                if (this.platformId) {
                    return {
                        platformId: this.platformId,
                    }
                }
                if (this.nodeId) {
                    return {
                        nodeId: this.nodeId,
                    }
                }
                return {}
            },
        },
    },
    name: "ChartUsersActiveRatio",
    mixins: [ChartMixin],
}
</script>
