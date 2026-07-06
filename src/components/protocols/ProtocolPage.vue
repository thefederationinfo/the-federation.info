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
                                <Number :number="nodes.length" />
                                <strong>Nodes</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="globalStats.users_total" />
                                <strong>Users</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="globalStats.local_posts" />
                                <strong>Posts</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="globalStats.local_comments" />
                                <strong>Comments</strong>
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
                                <li>Nodes: <strong><Number :number="nodes.length" /></strong></li>
                                <li>Users: <strong><Number :number="globalStats.users_total" /></strong></li>
                                <li>Last 6 months users: <strong><Number :number="globalStats.users_half_year" /></strong></li>
                                <li>Last month users: <strong><Number :number="globalStats.users_monthly" /></strong></li>
                                <li>Posts: <strong><Number :number="globalStats.local_posts" /></strong></li>
                                <li>Comments: <strong><Number :number="globalStats.local_comments" /></strong></li>
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
                <NodeSearchBox @search="onSearch" />
                <div class="overflow-x">
                    <NodesTable
                        :nodes="filteredTableNodes"
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
import Number from "../common/Number"
import NodeSearchBox from "../common/NodeSearchBox"
import NodesTable from "../NodesTable"

const query = gql`
query MyQuery($id: Int!, $yesterday: date!) {
    thefederation_protocol_by_pk(id: $id) {
        name
        description
        website
        display_name
        thefederation_node_protocols(where: {thefederation_node: {blocked: {_eq: false}, hide_from_list: {_eq: false}, thefederation_stats: {date: {_eq: $yesterday}}}}) {
            thefederation_node {
                id
                name
                version
                open_signups
                host
                country
                thefederation_platform {
                    name
                }
                thefederation_node_services {
                    thefederation_service {
                        name
                    }
                }
                thefederation_stats_aggregate(where: {date: {_eq: $yesterday}}) {
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
        thefederation_stats_aggregate(where: {date: {_eq: $yesterday}}) {
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
`

export default {
    apollo: {
        queries: {
            query,
            manual: true,
            result({data}) {
                this.protocol = data.thefederation_protocol_by_pk
                this.nodes = data.thefederation_protocol_by_pk.thefederation_node_protocols
                this.tableNodes = data.thefederation_protocol_by_pk.thefederation_node_protocols.map((n) => n.thefederation_node)
                this.globalStats = data.thefederation_protocol_by_pk.thefederation_stats_aggregate.aggregate.avg || {}
            },
            variables() {
                const date = new Date()
                return {
                    id: this.$route.params.protocol,
                    yesterday: new Date(new Date().setDate(date.getDate() - 1)),
                }
            },
        },
    },
    name: "ProtocolPage",
    components: {
        ApolloLoader, NodeSearchBox, NodesTable, Footer, Drawer, Number,
    },
    data() {
        return {
            globalStats: {},
            nodes: [],
            protocol: {},
            search: '',
            tableNodes: [],
        }
    },
    computed: {
        // This page loads all nodes in a single query, so the search
        // filters client side. Stat counts above keep using the full
        // list, only the table reacts to the search.
        filteredTableNodes() {
            if (!this.search) {
                return this.tableNodes
            }
            const term = this.search.toLowerCase()
            return this.tableNodes.filter(
                (node) => (node.name || '').toLowerCase().includes(term),
            )
        },
        title() {
            return this.protocol.display_name ? this.protocol.display_name : this.protocol.name || ''
        },
    },
    methods: {
        onSearch(term) {
            this.search = term
        },
    },
}
</script>
