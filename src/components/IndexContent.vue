<template>
    <div>
        <main>
            <header class="main-header">
                <div class="main-title">
                    <h1>
                        <router-link to="/">
                            The Federation
                        </router-link>
                    </h1>
                    <h2>Welcome to the new social web</h2>
                </div>
                <div class="flex">
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="protocols.length" />
                                <strong>Protocols</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            <ApolloLoader :loading="$apollo.loading">
                                <Number :number="platforms.length" />
                                <strong>Projects</strong>
                            </ApolloLoader>
                        </div>
                    </div>
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
                                <Number :number="statsGlobalToday.users_total ? statsGlobalToday.users_total : null" />
                                <strong>Users</strong>
                            </ApolloLoader>
                        </div>
                    </div>
                </div>
            </header>

            <section class="tile">
                <header>
                    <h2>What is The Federation?</h2>
                </header>
                <div>
                    <div class="flex">
                        <div class="col2">
                            <p>
                                The Federation, or as often called the "Fediverse", refers to a global social network
                                composed of nodes that talk to each other. Each of them is an installation of software
                                which supports one of the federated social web protocols.
                            </p>
                            <p>
                                These social hubs create a decentralized and federated social network of millions
                                of users all around the globe. This is how the internet was supposed to be.
                            </p>
                            <div class="center">
                                <router-link
                                    to="/nodes"
                                    class="btn btn-primary"
                                >
                                    Nodes list
                                </router-link>
                            </div>
                        </div>
                        <div class="col2">
                            <ApolloLoader :loading="$apollo.loading">
                                <ul>
                                    <li>
                                        Nodes:
                                        <strong><Number :number="nodeCount" /></strong>
                                    </li>
                                    <li>
                                        Users:
                                        <strong>
                                            <Number :number="statsGlobalToday.users_total ? statsGlobalToday.users_total : null" />
                                        </strong>
                                    </li>
                                    <li>
                                        Last 6 months active users:
                                        <strong>
                                            <Number
                                                :number="statsGlobalToday.users_half_year ? statsGlobalToday.users_half_year : null"
                                            />
                                        </strong>
                                    </li>
                                    <li>
                                        Last month active users:
                                        <strong>
                                            <Number
                                                :number="statsGlobalToday.users_monthly ? statsGlobalToday.users_monthly : null"
                                            />
                                        </strong>
                                    </li>
                                    <li>
                                        Posts:
                                        <strong>
                                            <Number :number="statsGlobalToday.local_posts ? statsGlobalToday.local_posts : null" />
                                        </strong>
                                    </li>
                                    <li>
                                        Comments:
                                        <strong>
                                            <Number
                                                :number="statsGlobalToday.local_comments ? statsGlobalToday.local_comments : null"
                                            />
                                        </strong>
                                    </li>
                                </ul>
                            </ApolloLoader>
                            <div>
                                <strong>Disclaimer:</strong> These counts do not reflect the whole network due to the
                                opt-in nature of the statistics.
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <Charts />

            <div id="projects" />
            <section class="tile">
                <header>
                    <h2>Projects</h2>
                </header>
                <div class="overflow-x">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 20px;" />
                                <th style="text-align: left;">
                                    Project
                                </th>
                                <th>Nodes</th>
                                <th>Users</th>
                                <th>Website</th>
                                <th>Code</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-for="platform in platforms">
                                <PlatformTableRow
                                    v-if="platform.id"
                                    :key="platform.id"
                                    :platform="platform"
                                />
                            </template>
                        </tbody>
                    </table>
                    <ApolloLoader :loading="$apollo.loading" />
                </div>
            </section>

            <div id="protocols" />
            <section class="tile">
                <header>
                    <h2>Protocols</h2>
                </header>
                <div class="overflow-x">
                    <table>
                        <thead>
                            <tr>
                                <th>Protocol</th>
                                <th>Nodes</th>
                                <th>Users</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-for="protocol in protocols">
                                <ProtocolTableRow
                                    v-if="protocol.id"
                                    :key="protocol.id"
                                    :protocol="protocol"
                                />
                            </template>
                        </tbody>
                    </table>
                    <ApolloLoader :loading="$apollo.loading" />
                </div>
            </section>

            <section class="tile">
                <header>
                    <h2>Be part of our world</h2>
                </header>
                <div class="flex">
                    <div class="col2">
                        <h3>Host yourself</h3>
                        <p>
                            You want to install your own node?
                            Awesome! Choose a project and follow an installation guide.
                        </p>
                        <div id="install-guides-list">
                            <div
                                v-for="platform in platforms"
                                :key="platform.id"
                            >
                                <div v-if="platform.installGuide">
                                    <a
                                        :href="platform.installGuide"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        {{ platform.displayName ? platform.displayName : platform.name }}
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col2">
                        <h3>I already have my node!</h3>
                        <p>
                            Yay! Welcome to the crew! To include your node on this website, please go to
                            <code>https://the-federation.info/register/&lt;yournode.tld&gt;</code>.
                            After some seconds, you should see your node added..
                        </p>
                    </div>
                </div>
            </section>
        </main>
    </div>
</template>

<script>
import gql from 'graphql-tag'

import ApolloLoader from "./common/ApolloLoader"
import Charts from "./Charts"
import Number from "./common/Number"
import PlatformTableRow from "./PlatformTableRow"
import ProtocolTableRow from "./ProtocolTableRow"

// TODO add failsafe if new day
const query = gql`
query IndextContent($today: date!, $yesterday: date!, $last_success: timestamptz!) {
    thefederation_node_aggregate(where: {last_success: {_gte: $last_success}, blocked: {_eq: false}}) {
        aggregate {
            count
        }
    }
    thefederation_platform(where: {thefederation_nodes: {last_success: {_gte: $last_success}, blocked: {_eq: false}}}, order_by: {thefederation_nodes_aggregate: {count: desc}}) {
        id
        code
        name
        icon
        display_name
        install_guide
        license
        website
        thefederation_nodes_aggregate(where: {thefederation_stats: {date: {_eq: $today}}}) {
            aggregate {
                count
            }
        }
        thefederation_stats(where: {date: {_eq: $today}}) {
            users_total
        }
    }
    thefederation_protocol(where: {thefederation_node_protocols: {thefederation_node: {blocked: {_eq: false}, last_success: {_gte: $last_success}}}}) {
        id
        name
        thefederation_stats(where: {date: {_eq: $today}}) {
            users_total
        }
        thefederation_node_protocols_aggregate {
            aggregate {
                count
            }
        }
    }
    thefederation_stat_aggregate(where: {node_id: {_is_null: true}, platform_id: {_is_null: true}, protocol_id: {_is_null: true}, date: {_gte: $yesterday}}) {
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
        allQueries: {
            query,
            variables: {
                today: new Date(),
                yesterday: new Date(new Date().setDate(new Date().getDate() - 1)),
                last_success: new Date(new Date().setDate(-30)),
            },
            result({data}) {
                this.nodeCount = data.thefederation_node_aggregate.aggregate.count
                this.platforms = data.thefederation_platform
                this.protocols = data.thefederation_protocol
                this.statsGlobalToday = data.thefederation_stat_aggregate.aggregate.avg
            },
            manual: true,
        },
    },
    name: "IndexContent",
    components: {
        ApolloLoader, Charts, PlatformTableRow, ProtocolTableRow, Number,
    },
    data() {
        return {
            nodeCount: 0,
            platforms: [],
            protocols: [],
            statsGlobalToday: [],
        }
    },
}
</script>

<style scoped>
    #install-guides-list {
        text-align: center;
    }
</style>
