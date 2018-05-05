<script>
import ChartMixin from "./ChartMixin"
import {getQuery} from "./utils"

export default {
    apollo: {
        stats: {
            query: getQuery('statsUsersMonthly'),
            manual: true,
            result({data}) {
                this.stats = data.statsUsersMonthly
            },
            variables() {
                return {
                    platform: this.platform,
                }
            },
        },
    },
    name: "ChartNodes",
    mixins: [ChartMixin],
}
</script>

<style scoped>

</style>
