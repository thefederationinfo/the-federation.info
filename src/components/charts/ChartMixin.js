import commonChartOptions from "./commonChartOptions"
import {lineChartTemplate} from "./utils"

export default {
    props: {
        label: {
            type: String,
            default: '',
        },
        item: {
            type: String,
            default: '',
        },
        type: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            stats: [],
        }
    },
    computed: {
        chartOptions() {
            return commonChartOptions
        },
        statsData() {
            const data = {}
            for (const o of this.stats) {
                data[o.date] = o.count
            }
            return [{
                data,
                name: this.label,
            }]
        },
    },
    template: lineChartTemplate,
}
