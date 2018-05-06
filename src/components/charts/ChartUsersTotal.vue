<script>
import ChartMixin from "./ChartMixin"
import {getQuery} from "./utils"

export default {
    apollo: {
        stats: {
            query: getQuery('statsUsersTotal'),
            manual: true,
            result({data}) {
                this.stats = data.statsUsersTotal
            },
            variables() {
                return {
                    platform: this.platform,
                }
            },
        },
    },
    name: "ChartUsersTotal",
    mixins: [ChartMixin],
}
</script>

<style scoped>

</style>
