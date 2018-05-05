<script>
import ChartMixin from "./ChartMixin"
import {getQuery} from "./utils"

export default {
    apollo: {
        stats: {
            query: getQuery('statsUsersHalfYear'),
            manual: true,
            result({data}) {
                this.stats = data.statsUsersHalfYear
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
