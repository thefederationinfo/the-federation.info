<template>
    <div>
        <Drawer />

        <main>
            <header class="main-header">
                <div class="main-title">
                    <h1>{{ title }}</h1>
                </div>
                <div class="flex">
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                {{ total || '' }} <strong>Nodes</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                {{ globalStats.usersTotal || '' }} <strong>Users</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                {{ globalStats.localPosts || '' }} <strong>Posts</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                {{ globalStats.localComments || '' }} <strong>Comments</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                </div>
            </header>
            <section class="tile">
                <header>
                    <h2>Info</h2>
                </header>
                <div>
                    <div class="flex">
                        <div class="col2">
                            <p>{{ protocol.description }}</p>
                            <div class="flex">
                                <div
                                    v-if="protocol.website"
                                    class="col2 center"
                                >
                                    <a
                                        :href="protocol.website"
                                        class="btn btn-primary"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        Website
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="col2">
                            <ul>
                                <li>Nodes: <strong>{{ total || '' }}</strong></li>
                                <li>Users: <strong>{{ globalStats.usersTotal || '' }}</strong></li>
                                <li>Last 6 months users: <strong>{{ globalStats.usersHalfYear || '' }}</strong></li>
                                <li>Last month users: <strong>{{ globalStats.usersMonthly || '' }}</strong></li>
                                <li>Posts: <strong>{{ globalStats.localPosts || '' }}</strong></li>
                                <li>Comments: <strong>{{ globalStats.localComments || '' }}</strong></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Disable charts for now on protocol page. Reason is that protocol is changing over time
                 thing. We can't for example count all mastodon servers towards activitypub since the
                 support for that is recent and even not landing on all servers at the same time. Some
                 platforms allow turning protocols on and off. If we want to show history charts, we
                 must store protocol history per node first. -->
            <!--<Charts
                v-if="protocol"
                :item="protocol.name"
                type="protocol"
            />-->

            <section class="tile">
                <header>
                    <h2>All {{ title }} nodes</h2>
                </header>
                <div class="overflow-x">
                    <NodesTable
                        :edges="nodes"
                        :stats="stats"
                        :pages="pages"
                        :page="page"
                        :rows="rows"
                        :total="total"
                        @search="search"
                        @next-page="getNextPage"
                        @prev-page="getPreviosuPage"
                        @get-page="getPage"
                    />
                    <ApolloLoader :loading="$apollo.loading" />
                </div>
            </section>
        </main>

        <Footer />
    </div>
</template>

<script>
import gql from 'graphql-tag'

import ApolloLoader from "../common/ApolloLoader"
import Drawer from "../common/Drawer"
import Footer from "../common/Footer"
import NodesTable from "../NodesTable"

const query = gql`
    query Protocol($name: String!, $first: Int!, $after: String!, $last: Int!, $before: String!, $search: String!) {
        protocols(name: $name) {
            name
        }

        nodes(protocol: $name, first: $first, after: $after, last: $last, before: $before, search: $search) {
            totalCount
            edges {
              node {
                    id
                    name
                    version
                    openSignups
                    host
                    platform {
                        name
                        icon
                    }
                    countryCode
                    countryFlag
                    countryName
                    services {
                        name
                    }
                }
            }
            pageInfo {
                hasNextPage
                hasPreviousPage
                startCursor
                endCursor
            }
        }

        statsGlobalToday(protocol: $name) {
            usersTotal
            usersHalfYear
            usersMonthly
            localPosts
            localComments
        }

        statsNodes(protocol: $name) {
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
        queries: {
            query,
            manual: true,
            result({data}) {
                this.nodes = data.nodes.edges
                this.total = data.nodes.totalCount
                this.pageInfo = data.nodes.pageInfo
                this.pages = Array(...{length: this.total / this.rows}).map(Number.call, Number)
                this.protocol = data.protocols[0] || {}
                const stats = {}
                for (const o of data.statsNodes) {
                    stats[o.node.id] = o
                }
                this.stats = stats
                this.globalStats = data.statsGlobalToday || {}
            },
            variables() {
                return {
                    name: this.$route.params.protocol,
                    first: this.rows,
                    after: "",
                    before: "",
                    last: this.rows,
                    search: "",
                }
            },
        },
    },
    name: "ProtocolPage",
    components: {
        ApolloLoader, NodesTable, Footer, Drawer,
    },
    data() {
        return {
            globalStats: {},
            nodes: [],
            protocol: {},
            stats: {},
            pageInfo: {},
            pages: [],
            rows: 50,
            total: 1,
            page: 1,
            variables: {},
            search_val: "",
        }
    },
    computed: {
        title() {
            return this.protocol.displayName ? this.protocol.displayName : this.protocol.name || ''
        },
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
        getPreviosuPage() {
            // I don't know why this works, if you have a better way (I bet you do) please do a PR
            this.variables = {
                first: this.rows * this.page,
                after: "",
                before: this.pageInfo.startCursor,
                last: this.rows,
                search: this.search_val,
            }
            this.getPage(this.page - 1)
        },
        getPage(page) {
            this.page = page
            this.nodes = []
            // Fetch more data and transform the original result
            this.$apollo.queries.queries.fetchMore({
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
