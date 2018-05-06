<template>
    <main>
        <header class="main-header">
            <div class="main-title">
                <h1><router-link to="/">The Federation</router-link></h1>
                <h2>Welcome to the new social web</h2>
            </div>
            <div class="flex">
                <div class="col4">
                    <div class="tile valign-wrapper">
                        {{ protocols.length }} <strong>Protocols</strong>
                    </div>
                </div>
                <div class="col4">
                    <div class="tile valign-wrapper">
                        {{ platforms.length }} <strong>Projects</strong>
                    </div>
                </div>
                <div class="col4">
                    <div class="tile valign-wrapper">
                        {{ nodes.length }} <strong>Nodes</strong>
                    </div>
                </div>
                <div class="col4">
                    <div class="tile valign-wrapper">
                        {{ statsGlobalToday ? statsGlobalToday.usersTotal : 0 }} <strong>Users</strong>
                    </div>
                </div>
                <div class="col4">
                    <div class="tile valign-wrapper">
                        ONE <strong>Network</strong>
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
                            The Federation refers to a global social network composed of nodes talking together.
                            Each of them is an installation of software which supports one of the federated social web
                            protocols.
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
                        <ul>
                            <li>
                                Nodes:
                                <strong>{{ nodes.length }}</strong>
                            </li>
                            <li>
                                Users:
                                <strong>{{ statsGlobalToday ? statsGlobalToday.usersTotal : 0 }}</strong>
                            </li>
                            <li>
                                Last 6 months active users:
                                <strong>{{ statsGlobalToday ? statsGlobalToday.usersHalfYear : 0 }}</strong>
                            </li>
                            <li>
                                Last month active users:
                                <strong>{{ statsGlobalToday ? statsGlobalToday.usersMonthly : 0 }}</strong>
                            </li>
                            <li>
                                Posts:
                                <strong>{{ statsGlobalToday ? statsGlobalToday.localPosts : 0 }}</strong>
                            </li>
                            <li>
                                Comments:
                                <strong>{{ statsGlobalToday ? statsGlobalToday.localComments : 0 }}</strong>
                            </li>
                        </ul>
                        <div>
                            <strong>Disclaimer:</strong> These counts do not reflect the whole network due to the
                            opt-in nature of the statistics.
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <Charts />

        <div id="projects"></div>
        <section class="tile">
            <header>
                <h2>Projects</h2>
            </header>
            <div class="overflow-x">
                <table>
                    <thead>
                        <tr>
                            <th>Project</th>
                            <th>Nodes</th>
                            <th>Users</th>
                            <th>Website</th>
                            <th>Code</th>
                        </tr>
                    </thead>
                    <tbody>
                        <PlatformTableRow
                            v-for="platform in platforms"
                            :key="platform.id"
                            :platform="platform"
                            :nodes="nodes"
                        />
                    </tbody>
                </table>
            </div>
        </section>

        <div id="protocols"></div>
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
                        <ProtocolTableRow
                            v-for="protocol in protocols"
                            :key="protocol.id"
                            :protocol="protocol"
                        />
                    </tbody>
                </table>
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
                        You want to install your own node? Awesome! Choose a project and follow an installation guide.
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
                        Yay! Welcome in the crew! To see your node included in this website, please go to
                        <code>https://the-federation.info/register/&lt;yournode.tld&gt;</code>.
                        After some seconds, you should see your node added..
                    </p>
                </div>
            </div>
        </section>
    </main>
</template>

<script>
import gql from 'graphql-tag'

import PlatformTableRow from "./PlatformTableRow"
import ProtocolTableRow from "./ProtocolTableRow"
import Charts from "./Charts"


const query = gql`
    query {
        nodes {
            id
            platform {
                name
            }
        }
        platforms {
            id
            code
            name
            displayName
            installGuide
            license
            website
        }
        protocols {
            id
            name
            nodes {
              name
            }
        }
        statsGlobalToday {
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
        allQueries: {
            query,
            result({data}) {
                this.nodes = data.nodes
                this.platforms = data.platforms
                this.protocols = data.protocols
                this.statsGlobalToday = data.statsGlobalToday
            },
            manual: true,
        },
    },
    name: "IndexContent",
    components: {Charts, PlatformTableRow, ProtocolTableRow},
    data() {
        return {
            nodes: [],
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
