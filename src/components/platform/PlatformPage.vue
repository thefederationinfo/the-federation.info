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
                            {{ nodes.length }} <strong>Nodes</strong>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            0 <strong>Users</strong>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            0 <strong>Posts</strong>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            0 <strong>Comments</strong>
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
                                <li>Nodes: <strong>0</strong></li>
                                <li>Users: <strong>0</strong></li>
                                <li>Last 6 months users: <strong>0</strong></li>
                                <li>Last month users: <strong>0</strong></li>
                                <li>Posts: <strong>0</strong></li>
                                <li>Comments: <strong>0</strong></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <Charts
                v-if="platform.name"
                :platform="platform.name"
            />

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

import Charts from "../Charts"
import Drawer from "../common/Drawer"
import Footer from "../common/Footer"
import NodesTable from "../NodesTable"

const query = gql`
    query Platform($name: String!) {
        platforms(name: $name) {
            name
            code
            displayName
            description
            tagline
            website
        }

        nodes(platform: $name) {
            id
            name
            version
            openSignups
            host
            platform {
              name
            }
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
                this.nodes = data.nodes
                this.platform = data.platforms[0] || {}
                const stats = {}
                for (const o of data.statsNodes) {
                    stats[o.node.id] = o
                }
                this.stats = stats
            },
            variables() {
                return {
                    name: this.$route.params.platform,
                }
            },
        },
    },
    name: 'PlatformPage',
    components: {Charts, NodesTable, Footer, Drawer},
    data() {
        return {
            nodes: [],
            platform: {},
            stats: {},
        }
    },
    computed: {
        title() {
            return this.platform.displayName ? this.platform.displayName : this.platform.name || ''
        },
    },
}
</script>

<style scoped>

</style>
