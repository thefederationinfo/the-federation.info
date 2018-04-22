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

export default {
    apollo: {
        nodes: query,
    },
    name: "NodesTable",
    components: {NodesTableRow},
    data() {
        return {
            nodes: [],
        }
    },
}
</script>

<style scoped>

</style>
