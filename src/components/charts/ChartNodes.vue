<template>
    <line-chart :data="nodes"></line-chart>
</template>

<script>
import gql from 'graphql-tag'

const query = gql`
    query {
        statsCountsNodes {
            date
            count
        }
    }
`

export default {
    apollo: {
        statsCountsNodes: query,
    },
    name: "ChartNodes",
    data() {
        return {
            statsCountsNodes: [],
        }
    },
    computed: {
        nodes() {
            const data = {}
            for (const o of this.statsCountsNodes) {
                data[o.date] = o.count
            }
            return [{
                data,
                name: 'Nodes',
            }]
        },
    },
}
</script>

<style scoped>

</style>
