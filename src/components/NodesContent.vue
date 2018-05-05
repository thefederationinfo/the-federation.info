<template>
    <main>
        <header class="main-header">
            <div class="main-title">
                <h1>The nodes</h1>
            </div>
        </header>
        <section class="tile">
            <header>
                <h2>List of nodes composing The Federation</h2>
            </header>
            <div>
                <p>You can also access list of nodes for each project using the global menu on the left.</p>
                <div class="overflow-x">
                    <NodesTable
                        :nodes="nodes"
                        :stats="stats"
                    />
                </div>
            </div>
        </section>
    </main>
</template>

<script>
import gql from 'graphql-tag'

import NodesTable from "./NodesTable"

const query = gql`
    query {
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
        allQueries: {
            query,
            result({data}) {
                this.nodes = data.nodes
                const stats = {}
                for (const o of data.statsNodes) {
                    stats[o.node.id] = o
                }
                this.stats = stats
            },
            manual: true,
        },
    },
    name: "NodesContent",
    components: {NodesTable},
    data() {
        return {
            nodes: [],
            stats: {},
        }
    },
}
</script>

<style scoped>

</style>
