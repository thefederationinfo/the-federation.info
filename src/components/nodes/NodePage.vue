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
                                {{ stats.usersTotal }} <strong>Users</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                {{ stats.usersMonthly }} <strong>Monthly users</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                {{ stats.localPosts }} <strong>Posts</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                {{ stats.localComments }} <strong>Comments</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                </div>
            </header>
            <section class="tile">
                <header>
                    <h2>Info</h2>
                    <div
                        v-if="node.platform.name === 'diaspora'"
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
                                        :to="{name: 'platform', params: {platform: node.platform.name}}"
                                        :title="platformTitle"
                                    >
                                        <strong>
                                            {{ platformTitle }}
                                        </strong>
                                    </router-link>
                                </li>
                                <li>Version: <strong>{{ node.version }}</strong></li>
                                <li>Open signups: <strong>{{ node.openSignups ? 'Yes' : 'No' }}</strong></li>
                                <!-- <li>Services: <strong>{{ node.services }}</strong></li> -->
                                <!-- <li>Protocols: <strong>{{ node.protocols }}</strong></li> -->
                                <li>Country: <strong>{{ node.country }}</strong></li>
                                <li>Services: <strong>{{ services }}</strong></li>
                            </ul>
                        </div>
                        <div class="col2">
                            <ul>
                                <li>Users: <strong>{{ stats.usersTotal }}</strong></li>
                                <li>Last 6 months active users: <strong>{{ stats.usersHalfYear }}</strong></li>
                                <li>Last month active users: <strong>{{ stats.usersMonthly }}</strong></li>
                                <li>Posts: <strong>{{ stats.localPosts }}</strong></li>
                                <li>Comments: <strong>{{ stats.localComments }}</strong></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <Charts
                v-if="node"
                :item="node.host"
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

const query = gql`
    query Node($host: String!) {
        nodes(host: $host) {
            name
            version
            openSignups
            host
            platform {
              name
              icon
              displayName
            }
            services {
                name
            }
        }

        statsNodes(host: $host) {
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
                this.node = data.nodes[0] || {}
                this.stats = data.statsNodes[0] || {}
            },
            variables() {
                return {
                    host: this.$route.params.host,
                }
            },
        },
    },
    name: "NodePage",
    components: {ApolloLoader, Charts, Footer, Drawer},
    data() {
        return {
            node: {
                platform: '',
            },
            stats: {},
        }
    },
    computed: {
        diasporaStatisticsUrl() {
            if (this.node.platform.name === 'diaspora' && this.node.host) {
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
            return this.node.platform.displayName ? this.node.platform.displayName : this.node.platform.name
        },
        services() {
            const services = []
            for (const o of this.node.services) {
                services.push(o.name)
            }
            return _.sortBy(services).join(', ')
        },
    },
}
</script>
