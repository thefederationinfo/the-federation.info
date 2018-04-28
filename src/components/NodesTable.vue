<template>
    <table id="nodes-table">
        <thead>
            <tr>
                <th>Software</th>
                <th>Name</th>
                <th>Version</th>
                <th>Open signups</th>
                <th>Total users</th>
                <th>Active users half year</th>
                <th>Active users monthly</th>
                <th>Local posts</th>
                <th>Local comments</th>
                <th>Services</th>
                <th>Country</th>
            </tr>
        </thead>
        <tbody>
            <NodesTableRow
                v-for="node in nodes"
                :node="node"
                :stats="statsForNode(node.id)"
                :key="node.id"
            />
        </tbody>
    </table>
</template>

<script>
import gql from 'graphql-tag'

import NodesTableRow from "./NodesTableRow"


const query = gql`
  {
      nodes {
        id
        name
        version
        openSignups
        host
        platform {
          name
        }
      }
  }
`

const statsQuery = gql`
    {
        statsNodes {
            node {
              id
            }
            usersTotal
            usersHalfYear
            usersMonthly
            localPosts
            localComments
        }
    }
`

export default {
    apollo: {
        nodes: query,
        statsNodes: {
            query: statsQuery,
            update(data) {
                const res = {}
                for (const o of data.statsNodes) {
                    res[o.node.id] = o
                }
                return res
            },
        },
    },
    name: "NodesTable",
    components: {NodesTableRow},
    data() {
        return {
            nodes: [],
            statsNodes: {},
        }
    },
    methods: {
        statsForNode(nodeId) {
            if (this.statsNodes[nodeId] === undefined) {
                return {
                    usersTotal: 0,
                    usersHalfYear: 0,
                    usersMonthly: 0,
                    localPosts: 0,
                    localComments: 0,
                }
            }
            return this.statsNodes[nodeId]
        },
    },
}
</script>

<style scoped>

</style>
