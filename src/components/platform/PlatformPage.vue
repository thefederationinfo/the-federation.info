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
                                <Number :number="nodeCount" />
                                <strong>Nodes</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="globalStats.users_total || 0" />
                                <strong>Users</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="globalStats.local_posts || 0" />
                                <strong>Posts</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="globalStats.local_comments || 0" />
                                <strong>Comments</strong>
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
                                <li>Nodes: <strong>{{ nodeCount || '' }}</strong></li>
                                <li>Users: <strong>{{ globalStats.users_total || '' }}</strong></li>
                                <li>Last 6 months users: <strong>{{ globalStats.users_half_year || '' }}</strong></li>
                                <li>Last month users: <strong>{{ globalStats.users_monthly || '' }}</strong></li>
                                <li>Posts: <strong>{{ globalStats.local_posts || '' }}</strong></li>
                                <li>Comments: <strong>{{ globalStats.local_comments || '' }}</strong></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <Charts
                v-if="platform.name"
                :item="platform.name"
                :platform-id="platform.id"
                type="platform"
            />

            <section class="tile">
                <header>
                    <h2>All {{ title }} nodes</h2>
                </header>
                <NodeSearchBox @search="onSearch" />
                <div class="overflow-x">
                    <NodesTable
                        :nodes="nodes"
                    />
                    <ApolloLoader :loading="$apollo.loading || loadingMore" />
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
import NodeSearchBox from "../common/NodeSearchBox"
import NodesTable from "../NodesTable"
import Number from "../common/Number"

const query = gql`
query PlatformDetails($id: Int!, $yesterday: date!, $pageSize: Int!, $pageOffset: Int!, $search: String!) {
    thefederation_platform_by_pk(id: $id) {
        id
        name
        code
        display_name
        description
        tagline
        website
    }
    nodeStats: thefederation_stat(where: {date: {_eq: $yesterday}, thefederation_node: {platform_id: {_eq: $id}, blocked: {_eq: false}, hide_from_list: {_eq: false}, name: {_ilike: $search}}}, order_by: {users_monthly: desc_nulls_last}, limit: $pageSize, offset: $pageOffset) {
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
            }
        }
    }
    nodeCount: thefederation_stat_aggregate(where: {date: {_eq: $yesterday}, thefederation_node: {platform_id: {_eq: $id}, blocked: {_eq: false}, hide_from_list: {_eq: false}}}) {
        aggregate {
            count
        }
    }
    filteredCount: thefederation_stat_aggregate(where: {date: {_eq: $yesterday}, thefederation_node: {platform_id: {_eq: $id}, blocked: {_eq: false}, hide_from_list: {_eq: false}, name: {_ilike: $search}}}) {
        aggregate {
            count
        }
    }
    thefederation_stat_aggregate(where: {thefederation_platform: {id: {_eq: $id}}, date: {_eq: $yesterday}}) {
        aggregate {
            avg {
                users_total
                users_half_year
                users_monthly
                users_weekly
                local_posts
                local_comments
            }
        }
    }
}
`

const pageSize = 50

export default {
    apollo: {
        platforms: {
            query,
            manual: true,
            result({data}) {
                this.platform = data.thefederation_platform_by_pk || {}
                // NodesTableRow expects node objects carrying their stats
                // under thefederation_stats_aggregate, keep that shape
                this.nodes = data.nodeStats.map(({thefederation_node: node, ...avg}) => ({
                    ...node,
                    thefederation_stats_aggregate: {aggregate: {avg}},
                }))
                this.nodeCount = data.nodeCount.aggregate.count
                this.filteredCount = data.filteredCount.aggregate.count
                this.globalStats = data.thefederation_stat_aggregate.aggregate.avg || {}
            },
            variables() {
                const date = new Date()
                const yesterday = new Date(new Date().setDate(date.getDate() - 1))
                return {
                    id: this.$route.params.platform,
                    yesterday,
                    pageSize,
                    pageOffset: 0,
                    search: this.searchPattern,
                }
            },
        },
    },
    name: 'PlatformPage',
    components: {
        ApolloLoader, Charts, NodeSearchBox, NodesTable, Footer, Drawer, Number,
    },
    data() {
        return {
            globalStats: {},
            nodes: [],
            platform: {},
            stats: {},
            nodeCount: 0,
            filteredCount: 0,
            search: '',
            currentPage: 0,
            loadingMore: false,
        }
    },
    computed: {
        title() {
            return this.platform.display_name ? this.platform.display_name : this.platform.name || ''
        },
        loadMoreEnabled() {
            return this.nodes.length < this.filteredCount
        },
        searchPattern() {
            // Escape ilike wildcards typed by the user, then wrap in %
            // so an empty search ("%%") matches every node
            return `%${this.search.replace(/[\\%_]/g, '\\$&')}%`
        },
    },
    mounted() {
        window.addEventListener('scroll', this.onScroll, {passive: true})
    },
    beforeDestroy() {
        window.removeEventListener('scroll', this.onScroll)
    },
    methods: {
        onSearch(term) {
            if (term === this.search) {
                return
            }
            // New search: back to page 0. Changing this.search changes
            // searchPattern, the reactive variables() re-run the query
            // and result() replaces the node list.
            this.currentPage = 0
            this.search = term
        },
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
            this.$apollo.queries.platforms.fetchMore({
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
