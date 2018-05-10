<script>
import ChartMixin from "./ChartMixin"
import {getQuery} from "./utils"

export default {
    apollo: {
        stats: {
            query: getQuery('statsLocalPosts'),
            manual: true,
            result({data}) {
                this.stats = data.statsLocalPosts
            },
            variables() {
                return {
                    type: this.type,
                    value: this.item,
                }
            },
        },
    },
    name: "ChartLocalPosts",
    mixins: [ChartMixin],
}
</script>
