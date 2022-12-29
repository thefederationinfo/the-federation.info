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
                                    <SortLink name="countryName">
                                        Country
                                    </SortLink>
                                </th>
                                <th>
                                    <SortLink name="count">
                                        Nodes
                                    </SortLink>
                                </th>
                                <th>
                                    <SortLink name="total">
                                        Total users
                                    </SortLink>
                                </th>
                                <th>
                                    <SortLink name="actives">
                                        Active users
                                    </SortLink>
                                </th>
                            </tr>
                        </thead>
                        <tbody
                            slot="body"
                            slot-scope="sort"
                        >
                            <tr
                                v-for="value in sort.values"
                                :key="value.id"
                            >
                                <td>
                                    {{ resolveCountryName(value.country) }} {{ resolveCountryFlag(value.country) }}
                                </td>
                                <td>
                                    <Number :number="value.count" />
                                </td>
                                <td>
                                    <Number :number="value.total" />
                                </td>
                                <td>
                                    <Number :number="value.actives" />
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

import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import ApolloLoader from "./common/ApolloLoader"
import Drawer from "./common/Drawer"
import Number from './common/Number'

const query = gql`
query HostingReport {
    hosting_report {
        country
        count
        total
        actives
    }
}
`

export default {
    apollo: {
        allQueries: {
            query,
            result({data}) {
                this.values = data.hosting_report
            },
            manual: true,
        },
    },
    name: "HostingReportPage",
    components: {ApolloLoader, Drawer, Number},
    data: () => ({values: []}),
    methods: {
        resolveCountryFlag(country) {
            if (country) {
                return getUnicodeFlagIcon(country)
            }
            return ''
        },
        resolveCountryName(country) {
            if (country) {
                const names = new Intl.DisplayNames(['en'], {type: 'region'})
                return names.of(country)
            }
            return ''
        },
    },
}
</script>

<style scoped>
    .center {
        text-align: center;
    }
</style>
