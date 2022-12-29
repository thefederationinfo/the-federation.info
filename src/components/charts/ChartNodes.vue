<script>
import gql from "graphql-tag"
import ChartMixin from "./ChartMixin"

const globalQuery = gql`
query Nodes {
    node_count_per_date(order_by: {date: desc}) {
        count
        date
    }
}
`

const platformQuery = gql`
query NodesByPlatform($platformid: Int!) {
    node_count_per_date_by_platform_id(args: {platformid: $platformid}, order_by: {date: desc}) {
        date
        count
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
                return globalQuery
            },
            manual: true,
            result({data}) {
                if (data.node_count_per_date) {
                    this.stats = data.node_count_per_date
                } else if (data.node_count_per_date_by_platform_id) {
                    this.stats = data.node_count_per_date_by_platform_id
                }
            },
            variables() {
                if (this.platformId) {
                    return {
                        platformid: this.platformId,
                    }
                }
                return {}
            },
        },
    },
    name: "ChartNodes",
    mixins: [ChartMixin],
}
</script>
