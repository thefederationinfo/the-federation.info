<template>
    <div>
        <Drawer />

        <main>
            <header class="main-header">
                <div class="main-title">
                    <h1>Hosting report</h1>
                </div>
            </header>
            <section class="tile">
                <header>
                    <h2>Where are the nodes at?</h2>
                </header>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>
                                    Country
                                </th>
                                <th>
                                    Nodes
                                </th>
                                <th>
                                    Total users
                                </th>
                                <th>
                                    Active users
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="country in stats"
                                :key="country.name"
                            >
                                <td>
                                    {{ country.name }}
                                </td>
                                <td>
                                    {{ country.nodes }}
                                </td>
                                <td>
                                    {{ country.total }}
                                </td>
                                <td>
                                    {{ country.active }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <ApolloLoader :loading="$apollo.loading" />
                </div>
            </section>
        </main>
    </div>
</template>

<script>
import gql from "graphql-tag"

import ApolloLoader from "./common/ApolloLoader"
import Drawer from "./common/Drawer"
import Footer from "./common/Footer"

const query = gql`
    query {
        nodes {
            id
            countryName
        }
        statsNodes {
            node {
                id
            }
            usersTotal
            usersHalfYear
        }
    }
`

export default {
    apollo: {
        allQueries: {
            query,
            result({data}) {
                const countries = {}
                const stats = {}
                for (const o of data.nodes) {
                    countries[o.id] = o.countryName
                    if (stats[o.countryName] === undefined) {
                        stats[o.countryName] = {
                            name: o.countryName,
                            total: 0,
                            active: 0,
                            nodes: 0,
                        }
                    }
                }
                for (const o of data.statsNodes) {
                    stats[countries[o.node.id]].nodes += 1
                    stats[countries[o.node.id]].total += o.usersTotal
                    stats[countries[o.node.id]].active += o.usersHalfYear
                }
                this.stats = stats
            },
            manual: true,
        },
    },
    name: "HostingReportPage",
    components: {ApolloLoader, Drawer, Footer},

    data: () => {
        return {
            stats: {},
        }
    },
}
</script>

<style scoped>

</style>
