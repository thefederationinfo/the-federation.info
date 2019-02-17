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
                    <SortedTable :values="values">
                        <thead>
                            <tr>
                                <th>
                                    <SortLink name="name">Country</SortLink>
                                </th>
                                <th>
                                    <SortLink name="nodes">Nodes</SortLink>
                                </th>
                                <th>
                                    <SortLink name="total">Total users</SortLink>
                                </th>
                                <th>
                                    <SortLink name="active">Active users</SortLink>
                                </th>
                            </tr>
                        </thead>
                        <tbody slot="body" slot-scope="sort">
                            <tr
                                v-for="value in sort.values"
                                :key="value.name"
                            >
                                <td>
                                    {{ value.name }}
                                </td>
                                <td>
                                    {{ value.nodes }}
                                </td>
                                <td>
                                    {{ value.total }}
                                </td>
                                <td>
                                    {{ value.active }}
                                </td>
                            </tr>
                        </tbody>
                    </SortedTable>
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
                const values = []
                for (const idx in stats) {
                    values.push(stats[idx])
                }
                this.values = values
            },
            manual: true,
        },
    },
    name: "HostingReportPage",
    components: {ApolloLoader, Drawer, Footer},

    data: () => {
        return {
            values: [],
        }
    },
}
</script>

<style scoped>

</style>
