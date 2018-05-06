<template>
    <section class="tile">
        <header>
            <h2>Charts</h2>
        </header>
        <div id="charts-buttons">
            <div
                v-if="type !== 'node'"
                :class="{selected: isSelected('nodes')}"
                class="btn-medium"
                @click="selectChart('nodes')"
            >
                Nodes
            </div>
            <div
                :class="{selected: isSelected('users_total')}"
                class="btn-medium"
                @click="selectChart('users_total')"
            >
                Total users
            </div>
            <div
                :class="{selected: isSelected('users_half_year')}"
                class="btn-medium"
                @click="selectChart('users_half_year')"
            >
                Active 6 months
            </div>
            <div
                :class="{selected: isSelected('users_monthly')}"
                class="btn-medium"
                @click="selectChart('users_monthly')"
            >
                Active last month
            </div>
            <div
                :class="{selected: isSelected('local_posts')}"
                class="btn-medium"
                @click="selectChart('local_posts')"
            >
                Local posts
            </div>
            <div
                :class="{selected: isSelected('local_comments')}"
                class="btn-medium"
                @click="selectChart('local_comments')"
            >
                Local comments
            </div>
        </div>
        <div>
            <ChartNodes
                v-if="isSelected('nodes')"
                :item="item"
                :type="type"
                label="Nodes"
            />
            <ChartUsersTotal
                v-if="isSelected('users_total')"
                :item="item"
                :type="type"
                label="Total users"
            />
            <ChartUsersHalfYear
                v-if="isSelected('users_half_year')"
                :item="item"
                :type="type"
                label="Active users 6 months"
            />
            <ChartUsersMonthly
                v-if="isSelected('users_monthly')"
                :item="item"
                :type="type"
                label="Active users last month"
            />
            <ChartLocalPosts
                v-if="isSelected('local_posts')"
                :item="item"
                :type="type"
                label="Total local posts"
            />
            <ChartLocalComments
                v-if="isSelected('local_comments')"
                :item="item"
                :type="type"
                label="Total local comments"
            />
        </div>
    </section>
</template>

<script>
import ChartNodes from "./charts/ChartNodes"
import ChartUsersTotal from "./charts/ChartUsersTotal"
import ChartUsersHalfYear from "./charts/ChartUsersHalfYear"
import ChartUsersMonthly from "./charts/ChartUsersMonthly"
import ChartLocalPosts from "./charts/ChartLocalPosts"
import ChartLocalComments from "./charts/ChartLocalComments"

export default {
    name: "Charts",
    components: {
        ChartNodes, ChartUsersTotal, ChartUsersHalfYear, ChartUsersMonthly, ChartLocalPosts, ChartLocalComments,
    },
    props: {
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
            activeChart: this.type === 'node' ? 'users_total' : 'nodes',
        }
    },
    methods: {
        isSelected(chart) {
            return chart === this.activeChart
        },
        selectChart(chart) {
            this.activeChart = chart
        },
    },
}
</script>

<style scoped>

</style>
