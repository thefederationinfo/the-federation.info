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
                    type: this.type,
                    value: this.item,
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
