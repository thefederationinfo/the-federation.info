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
                            {{ nodes.length }} <strong>Nodes</strong>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            {{ globalStats.usersTotal || 0 }} <strong>Users</strong>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            {{ globalStats.localPosts || 0 }} <strong>Posts</strong>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            {{ globalStats.localComments || 0 }} <strong>Comments</strong>
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
                                <li>Nodes: <strong>{{ nodes.length }}</strong></li>
                                <li>Users: <strong>{{ globalStats.usersTotal || 0 }}</strong></li>
                                <li>Last 6 months users: <strong>{{ globalStats.usersHalfYear || 0 }}</strong></li>
                                <li>Last month users: <strong>{{ globalStats.usersMonthly || 0 }}</strong></li>
                                <li>Posts: <strong>{{ globalStats.localPosts || 0 }}</strong></li>
                                <li>Comments: <strong>{{ globalStats.localComments || 0 }}</strong></li>
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
                        :nodes="nodes"
                        :stats="stats"
                    />
                </div>
            </section>
        </main>

        <Footer />
    </div>
</template>

<script>
import gql from 'graphql-tag'

import Drawer from "../common/Drawer"
import Footer from "../common/Footer"
import NodesTable from "../NodesTable"

const query = gql`
    query Protocol($name: String!) {
        protocols(name: $name) {
            name
        }

        nodes(protocol: $name) {
            id
            name
            version
            openSignups
            host
            platform {
              name
            }
            countryCode
            countryFlag
            countryName
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
                this.nodes = data.nodes
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
                }
            },
        },
    },
    name: "ProtocolPage",
    components: {NodesTable, Footer, Drawer},
    data() {
        return {
            globalStats: {},
            nodes: [],
            protocol: {},
            stats: {},
        }
    },
    computed: {
        title() {
            return this.protocol.displayName ? this.protocol.displayName : this.protocol.name || ''
        },
    },
}
</script>

<style scoped>

</style>
