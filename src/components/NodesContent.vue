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
                    <NodesTable />
                    <ApolloLoader :loading="$apollo.loading" />
                </div>
            </div>
        </section>
    </main>
</template>

<script>
import gql from 'graphql-tag'

import ApolloLoader from "./common/ApolloLoader"
import NodesTable from "./NodesTable"

const query = gql`
    query NodeStatus {
        nodes {
            totalCount
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
                this.total = data.nodes.totalCount
                this.pages = Array(...{length: this.total / this.rows}).map(Number.call, Number)
                const stats = {}
                for (const o of data.statsNodes) {
                    stats[o.node.id] = o
                }
                this.stats = stats
            },
            manual: true,
            variables() {
                return {
                    first: this.rows,
                    after: "",
                    before: "",
                    last: this.rows,
                    search: "",
                }
            },
        },
    },
    name: "NodesContent",
    components: {ApolloLoader, NodesTable},
    data() {
        return {
            pageInfo: {},
            nodes: [],
            stats: {},
            pages: [],
            rows: 50,
            total: 1,
            page: 1,
            variables: {},
            search_val: "",
        }
    },
    methods: {
        search(value) {
            this.search_val = value
            this.variables.search = this.search_val
            this.getPage(1)
        },
        getNextPage() {
            this.variables = {
                first: this.rows,
                after: this.pageInfo.endCursor,
                before: "",
                last: this.rows,
                search: this.search_val,
            }
            this.getPage(this.page + 1)
        },
        getPreviousPage() {
            // I don't know why this works, if you have a better way (I bet you do) please do a PR
            this.variables = {
                first: this.rows * this.page,
                after: "",
                before: this.pageInfo.startCursor,
                last: this.rows,
                name: this.search_val,
            }
            this.getPage(this.page - 1)
        },
        getPage(page) {
            this.page = page
            this.nodes = []
            // Fetch more data and transform the original result
            this.$apollo.queries.allQueries.fetchMore({
                // New variables
                variables: this.variables,
                // Transform the previous result with new data
                updateQuery: (previousResult, {fetchMoreResult}) => {
                    this.pageInfo = fetchMoreResult.nodes.pageInfo
                    return fetchMoreResult
                },
            })
        },
    },
}
</script>
