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
                    type: this.type,
                    value: this.item,
                }
            },
        },
    },
    name: "ChartUsersMonthly",
    mixins: [ChartMixin],
}
</script>
