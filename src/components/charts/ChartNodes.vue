<script>
import ChartMixin from "./ChartMixin"
import {getQuery} from "./utils"

export default {
    apollo: {
        stats: {
            query: getQuery('statsCountsNodes'),
            manual: true,
            result({data}) {
                this.stats = data.statsCountsNodes
            },
            variables() {
                return {
                    type: this.type,
                    value: this.item,
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
