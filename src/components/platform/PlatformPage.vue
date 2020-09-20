<template>
    <div>
        <Drawer />
        <main>
            <header class="main-header">
                <div class="main-title">
                    <h1>{{ title }}</h1>
                    <h2>{{ platform.tagline }}</h2>
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
                                {{ globalStats.usersTotal || 0 }} <strong>Users</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                {{ globalStats.localPosts || 0 }} <strong>Posts</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                {{ globalStats.localComments || 0 }} <strong>Comments</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                </div>
            </header>
            <section class="tile">
                <header>
                    <h2>What is {{ title }}?</h2>
                </header>
                <div>
                    <div class="flex">
                        <div class="col2">
                            <p>{{ platform.description }}</p>
                            <div class="flex">
                                <div
                                    v-if="platform.website"
                                    class="col2 center"
                                >
                                    <a
                                        :href="platform.website"
                                        class="btn btn-primary"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        Official website
                                    </a>
                                </div>
                                <div
                                    v-if="platform.code"
                                    class="col2 center"
                                >
                                    <a
                                        :href="platform.code"
                                        class="btn"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        Source code
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

            <Charts
                v-if="platform.name"
                :item="platform.name"
                type="platform"
            />

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
import Charts from "../Charts"
import Drawer from "../common/Drawer"
import Footer from "../common/Footer"
import NodesTable from "../NodesTable"

const query = gql`
    query Platform($name: String!, $first: Int!, $after: String!, $last: Int!, $before: String!, $search: String!) {
        platforms(name: $name) {
            name
            code
            displayName
            description
            tagline
            website
            icon
        }

        nodes(platform: $name, first: $first, after: $after, last: $last, before: $before, search: $search) {
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

        statsGlobalToday(platform: $name) {
            usersTotal
            usersHalfYear
            usersMonthly
            localPosts
            localComments
        }

        statsNodes(platform: $name) {
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
                this.platform = data.platforms[0] || {}
                const stats = {}
                for (const o of data.statsNodes) {
                    stats[o.node.id] = o
                }
                this.stats = stats
                this.globalStats = data.statsGlobalToday || {}
            },
            variables() {
                return {
                    name: this.$route.params.platform,
                    first: this.rows,
                    after: "",
                    before: "",
                    last: this.rows,
                    search: "",
                }
            },
        },
    },
    name: 'PlatformPage',
    components: {
        ApolloLoader, Charts, NodesTable, Footer, Drawer,
    },
    data() {
        return {
            globalStats: {},
            nodes: [],
            platform: {},
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
            return this.platform.displayName ? this.platform.displayName : this.platform.name || ''
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
