<script>
import ChartMixin from "./ChartMixin"
import {getQuery} from "./utils"

export default {
    apollo: {
        stats: {
            query: getQuery('statsLocalComments'),
            manual: true,
            result({data}) {
                this.stats = data.statsLocalComments
            },
            variables() {
                return {
                    platform: this.platform,
                }
            },
        },
    },
    name: "ChartLocalComments",
    mixins: [ChartMixin],
}
</script>

<style scoped>

</style>
