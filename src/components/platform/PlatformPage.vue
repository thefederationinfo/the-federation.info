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
                        :platform="$route.params.platform"
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
    query Platform($name: String!) {
        platforms(name: $name) {
            name
            code
            displayName
            description
            tagline
            website
            icon
        }

        nodes(platform: $name) {
            totalCount
        }

        statsGlobalToday(platform: $name) {
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
                this.total = data.nodes.totalCount
                this.pageInfo = data.nodes.pageInfo
                this.platform = data.platforms[0] || {}
                this.globalStats = data.statsGlobalToday || {}
            },
            variables() {
                return {
                    name: this.$route.params.platform,
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
            total: 0,
            globalStats: {},
            platform: {},
        }
    },
    computed: {
        title() {
            return this.platform.displayName ? this.platform.displayName : this.platform.name || ''
        },
    },
}
</script>
