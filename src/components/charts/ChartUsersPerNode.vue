<script>
import ChartMixin from "./ChartMixin"
import {getQuery} from "./utils"

export default {
    apollo: {
        stats: {
            query: getQuery('statsUsersPerNode'),
            manual: true,
            result({data}) {
                this.stats = data.statsUsersPerNode
            },
            variables() {
                return {
                    type: this.type,
                    value: this.item,
                }
            },
        },
    },
    name: "ChartUsersPerNode",
    mixins: [ChartMixin],
}
</script>

<style scoped>

</style>
