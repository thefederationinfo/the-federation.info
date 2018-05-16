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
                    type: this.type,
                    value: this.item,
                }
            },
        },
    },
    name: "ChartUsersHalfYear",
    mixins: [ChartMixin],
}
</script>
