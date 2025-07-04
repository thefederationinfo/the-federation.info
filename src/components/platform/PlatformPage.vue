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
                                <Number :number="nodes.length" />
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
                                <li>Nodes: <strong>{{ nodes.length || '' }}</strong></li>
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
                <div class="overflow-x">
                    <NodesTable
                        :nodes="nodes"
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
import Number from "../common/Number"

const query = gql`
query PlatformDetails($id: Int!, $last_success: timestamptz!, $yesterday: date!) {
    thefederation_platform_by_pk(id: $id) {
        id
        name
        code
        display_name
        description
        tagline
        website
        icon
        thefederation_nodes(where: {blocked: {_eq: false}, hide_from_list: {_eq: false}, last_success: {_gte: $last_success}}, order_by: {thefederation_stats_aggregate: {max: {users_monthly: desc_nulls_last}}}) {
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
            thefederation_stats_aggregate(where: {date: {_gte: $yesterday}}) {
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
    }
    thefederation_stat_aggregate(where: {thefederation_platform: {id: {_eq: $id}}, date: {_gte: $yesterday}}) {
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

export default {
    apollo: {
        queries: {
            query,
            manual: true,
            result({data}) {
                this.icon = data.thefederation_platform_by_pk.icon
                this.nodes = data.thefederation_platform_by_pk.thefederation_nodes
                this.platform = data.thefederation_platform_by_pk || {}
                this.globalStats = data.thefederation_stat_aggregate.aggregate.avg || {}
            },
            variables() {
                const date = new Date()
                const yesterday = new Date(new Date().setDate(date.getDate() - 1))
                return {
                    id: this.$route.params.platform,
                    last_success: new Date(new Date().setDate(-30)),
                    yesterday,
                }
            },
        },
    },
    name: 'PlatformPage',
    components: {
        ApolloLoader, Charts, NodesTable, Footer, Drawer, Number,
    },
    data() {
        return {
            globalStats: {},
            nodes: [],
            platform: {},
            stats: {},
        }
    },
    computed: {
        title() {
            return this.platform.display_name ? this.platform.display_name : this.platform.name || ''
        },
    },
}
</script>
