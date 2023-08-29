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
                <p>You can also access a list of nodes for each project using the global menu on the left.</p>
                <div class="overflow-x">
                    <p><b>Currently unavailable!</b></p>
                </div>
            </div>
        </section>
    </main>
</template>

<script>
import gql from 'graphql-tag'

// The Node Table is just too big to create a query without pagination
const query = gql`
    query NodeContent {
        thefederation_node(where: {blocked: {_eq: false}, hide_from_list: {_eq: false}}) {
            id
            name
            version
            open_signups
            host
            country
            thefederation_platform {
                name
                icon
            }
            thefederation_node_services {
                thefederation_service {
                    name
                }
            }
        }
}
`

export default {
    apollo: {
        allQueries: {
            query,
            result({data}) {
                this.nodes = data.thefederation_node
                const stats = {}
                for (const o of data.thefederation_stat) {
                    if (o.thefederation_node) {
                        stats[o.thefederation_node.id] = o
                    }
                }
                this.stats = stats
            },
            manual: true,
        },
    },
    name: "NodesContent",
    data() {
        return {
            nodes: [],
            stats: {},
        }
    },
}
</script>
