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
                    <SortedTable
                        :values="values"
                        dir="desc"
                        sort="count"
                    >
                        <thead>
                            <tr>
                                <th class="center">
                                    <SortLink name="countryName">Country</SortLink>
                                </th>
                                <th>
                                    <SortLink name="count">Nodes</SortLink>
                                </th>
                                <th>
                                    <SortLink name="total">Total users</SortLink>
                                </th>
                                <th>
                                    <SortLink name="actives">Active users</SortLink>
                                </th>
                            </tr>
                        </thead>
                        <tbody
                            slot="body"
                            slot-scope="sort"
                        >
                            <tr
                                v-for="value in sort.values"
                                :key="value.name"
                            >
                                <td>
                                    {{ value.countryName }} {{ value.countryFlag }}
                                </td>
                                <td>
                                    {{ value.count }}
                                </td>
                                <td>
                                    {{ value.total }}
                                </td>
                                <td>
                                    {{ value.actives }}
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
        countryStats {
            actives
            total
            count
            countryFlag
            countryName
        }
    }
`

export default {
    apollo: {
        allQueries: {
            query,
            result({data}) {
                this.values = data.countryStats
            },
            manual: true,
        },
    },
    name: "HostingReportPage",
    components: {ApolloLoader, Drawer, Footer},

    data: () => ({values: []}),
}
</script>

<style scoped>
    .center {
        text-align: center;
    }
</style>
