<template>
    <div>
        <Drawer />

        <main>
            <header class="main-header">
                <div class="main-title">
                    <h1>{{ node.name }}</h1>
                    <h2>
                        <a
                            :href="nodeHost"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            {{ node.host }}
                        </a>
                    </h2>
                </div>
                <div class="flex">
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="stats.users_total" />
                                <strong>Users</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="stats.users_monthly" />
                                <strong>Monthly users</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="stats.local_posts" />
                                <strong>Posts</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="stats.local_comments" />
                                <strong>Comments</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                </div>
            </header>
            <section class="tile">
                <header>
                    <h2>Info</h2>
                    <div
                        v-if="node.thefederation_platform.name === 'diaspora'"
                        class="center right-action"
                    >
                        Access
                        <a
                            :href="diasporaStatisticsUrl"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            real time stats
                        </a>
                    </div>
                </header>
                <div>
                    <div class="flex">
                        <div class="col2">
                            <ul>
                                <li>
                                    Software:
                                    <router-link
                                        v-if="node.thefederation_platform"
                                        :to="{name: 'platform', params: {platform: node.thefederation_platform.id}}"
                                        :title="platformTitle"
                                    >
                                        <strong>
                                            {{ platformTitle }}
                                        </strong>
                                    </router-link>
                                </li>
                                <li>Version: <strong>{{ node.version }}</strong></li>
                                <li>Open signups: <strong>{{ node.open_signups ? 'Yes' : 'No' }}</strong></li>
                                <!-- <li>Services: <strong>{{ node.services }}</strong></li> -->
                                <!-- <li>Protocols: <strong>{{ node.protocols }}</strong></li> -->
                                <li>Country: <strong>{{ node.country }}</strong></li>
                                <li>Services: <strong>{{ services }}</strong></li>
                            </ul>
                        </div>
                        <div class="col2">
                            <ul>
                                <li>Users: <strong><Number :number="stats.users_total" /></strong></li>
                                <li>Last 6 months active users: <strong><Number :number="stats.users_half_year" /></strong></li>
                                <li>Last month active users: <strong><Number :number="stats.users_monthly" /></strong></li>
                                <li>Posts: <strong><Number :number="stats.local_posts" /></strong></li>
                                <li>Comments: <strong><Number :number="stats.local_comments" /></strong></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <Charts
                v-if="node"
                :item="node.host"
                :node-id="node.id"
                type="node"
            />
        </main>

        <Footer />
    </div>
</template>

<script>
import gql from 'graphql-tag'
import _ from "lodash/collection"

import ApolloLoader from "../common/ApolloLoader"
import Charts from "../Charts"
import Drawer from "../common/Drawer"
import Footer from "../common/Footer"
import Number from "../common/Number"

const query = gql`
query Node($id: Int!, $today: date!) {
    thefederation_node_by_pk(id: $id) {
        id
        name
        version
        open_signups
        host
        country
        thefederation_platform {
            id
            name
            icon
            display_name
        }
        thefederation_node_services {
            thefederation_service {
                name
            }
        }
        thefederation_stats(where: {date: {_eq: $today}}) {
            users_total
            users_half_year
            users_monthly
            users_weekly
            local_posts
            local_comments
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
                this.node = data.thefederation_node_by_pk || {}
                this.stats = this.node.thefederation_stats[0] || {}
            },
            variables() {
                return {
                    id: this.$route.params.id,
                    today: new Date(),
                }
            },
        },
    },
    name: "NodePage",
    components: {
        ApolloLoader, Charts, Footer, Drawer, Number,
    },
    data() {
        return {
            node: {
                thefederation_platform: '',
                thefederation_node_services: {
                    thefederation_service: [],
                },
                thefederation_stats: {},
            },
            stats: {},
        }
    },
    computed: {
        diasporaStatisticsUrl() {
            if (this.node.thefederation_platform.name === 'diaspora' && this.node.host) {
                return `https://${this.node.host}/statistics`
            }
            return ''
        },
        nodeHost() {
            if (this.node.host) {
                return `https://${this.node.host}`
            }
            return ''
        },
        platformTitle() {
            return this.node.thefederation_platform.display_name ? this.node.thefederation_platform.display_name : this.node.thefederation_platform.name
        },
        services() {
            const services = []
            for (const o of Object.assign([], this.node.thefederation_node_services)) {
                services.push(o.thefederation_service.name)
            }
            if (services.length === 0) {
                return '-'
            }
            return _.sortBy(services).join(', ')
        },
    },
}
</script>
