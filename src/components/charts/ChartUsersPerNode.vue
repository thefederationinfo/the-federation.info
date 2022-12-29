<script>
import gql from "graphql-tag"
import ChartMixin from "./ChartMixin"

const query = gql`
query UsersPerNode {
    users_per_node(order_by: {date: desc}) {
        count
        date
    }
}
`

const platformQuery = gql`
query UsersPerNodeByPlatform($platformId: Int!) {
    users_per_node_by_platform(args: {platformid: $platformId}, order_by: {date: desc}) {
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
                return query
            },
            manual: true,
            result({data}) {
                if (this.platformId) {
                    this.stats = data.users_per_node_by_platform
                } else {
                    this.stats = data.users_per_node
                }
            },
            variables() {
                if (this.platformId) {
                    return {
                        platformId: this.platformId,
                    }
                }
                return {}
            },
        },
    },
    name: "ChartUsersPerNode",
    mixins: [ChartMixin],
}
</script>
