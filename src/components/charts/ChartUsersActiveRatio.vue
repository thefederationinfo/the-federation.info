<script>
import ChartMixin from "./ChartMixin"
import {getQuery} from "./utils"

export default {
    apollo: {
        stats: {
            query: getQuery('statsUsersActiveRatio'),
            manual: true,
            result({data}) {
                this.stats = data.statsUsersActiveRatio
            },
            variables() {
                return {
                    type: this.type,
                    value: this.item,
                }
            },
        },
    },
    name: "ChartUsersActiveRatio",
    mixins: [ChartMixin],
}
</script>
