<template>
    <main>
        <header class="main-header">
            <div class="main-title">
                <h1>The nodes</h1>
            </div>
        </header>
        <section class="tile">
            <header>
                <h2>List of nodes composing The Federation ({{ nodeCount }})</h2>
            </header>
            <div>
                <p>You can also access a list of nodes for each project using the global menu on the left.</p>
                <div class="overflow-x">
                    <NodesTable
                        :nodes="nodes"
                    />
                    <ApolloLoader :loading="$apollo.loading || loadingMore" />
                </div>
            </div>
        </section>
    </main>
</template>

<script>
import gql from 'graphql-tag'

import ApolloLoader from "./common/ApolloLoader"
import NodesTable from "./NodesTable"

// Paginate over yesterday's stat rows instead of the node table: one row
// per node, cheap to order by size, and limit/offset actually limit the
// work. The unpaginated node query is why this page was disabled before.
const query = gql`
query NodesContent($last_success: timestamptz!, $yesterday: date!, $pageSize: Int!, $pageOffset: Int!) {
    nodeStats: thefederation_stat(where: {date: {_eq: $yesterday}, thefederation_node: {blocked: {_eq: false}, hide_from_list: {_eq: false}, last_success: {_gte: $last_success}}}, order_by: {users_monthly: desc_nulls_last}, limit: $pageSize, offset: $pageOffset) {
        users_total
        users_half_year
        users_monthly
        users_weekly
        local_posts
        local_comments
        thefederation_node {
            id
            name
            open_signups
            host
            country
            version
            thefederation_node_services {
                thefederation_service {
                    name
                }
            }
            thefederation_platform {
                name
                icon
            }
        }
    }
    nodeCount: thefederation_stat_aggregate(where: {date: {_eq: $yesterday}, thefederation_node: {blocked: {_eq: false}, hide_from_list: {_eq: false}, last_success: {_gte: $last_success}}}) {
        aggregate {
            count
        }
    }
}
`

const pageSize = 50

export default {
    apollo: {
        nodesQuery: {
            query,
            manual: true,
            result({data}) {
                // NodesTableRow expects node objects carrying their stats
                // under thefederation_stats_aggregate, keep that shape
                this.nodes = data.nodeStats.map(({thefederation_node: node, ...avg}) => ({
                    ...node,
                    thefederation_stats_aggregate: {aggregate: {avg}},
                }))
                this.nodeCount = data.nodeCount.aggregate.count
            },
            variables() {
                const date = new Date()
                const yesterday = new Date(new Date().setDate(date.getDate() - 1))
                return {
                    last_success: new Date(new Date().setDate(-30)),
                    yesterday,
                    pageSize,
                    pageOffset: 0,
                }
            },
        },
    },
    name: "NodesContent",
    components: {
        ApolloLoader, NodesTable,
    },
    data() {
        return {
            nodes: [],
            nodeCount: 0,
            currentPage: 0,
            loadingMore: false,
        }
    },
    computed: {
        loadMoreEnabled() {
            return this.nodes.length < this.nodeCount
        },
    },
    mounted() {
        window.addEventListener('scroll', this.onScroll, {passive: true})
    },
    beforeDestroy() {
        window.removeEventListener('scroll', this.onScroll)
    },
    methods: {
        onScroll() {
            if (!this.loadMoreEnabled || this.loadingMore) {
                return
            }
            const nearBottom = window.innerHeight + window.pageYOffset
                >= document.documentElement.scrollHeight - 600
            if (nearBottom) {
                this.loadMore()
            }
        },
        loadMore() {
            if (this.loadingMore || !this.loadMoreEnabled) {
                return
            }
            this.loadingMore = true
            this.currentPage += 1

            // Fetch the next page and append it to the already loaded rows.
            // result() runs again after the merge; if the viewport is still
            // near the bottom the scroll handler chains the next page.
            this.$apollo.queries.nodesQuery.fetchMore({
                variables: {
                    pageOffset: pageSize * this.currentPage,
                    pageSize,
                },
                updateQuery: (data, {fetchMoreResult: newData}) => {
                    newData.nodeStats = [...data.nodeStats, ...newData.nodeStats]

                    return newData
                },
            }).finally(() => {
                this.loadingMore = false
                this.onScroll()
            })
        },
    },
}
</script>
