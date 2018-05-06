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
                    platform: this.platform,
                }
            },
        },
    },
    name: "ChartLocalPosts",
    mixins: [ChartMixin],
}
</script>

<style scoped>

</style>
