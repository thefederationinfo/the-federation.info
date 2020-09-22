<template>
    <div>
        <div class="search-box">
            <input
                v-model="searchVal"
                aria-label="search box"
                type="text"
                placeholder="Search node name"
                class="search-bar"
                @keyup.enter="search"
            >
            <button
                aria-label="Search Button"
                class="nav-btn"
                @click="search"
            >
                Search
            </button>
        </div><br>
        <nav
            aria-label="Page navigation"
            class="nav"
        >
            <span class="page-item">
                <button
                    :disabled="page === 1"
                    class="nav-btn prev"
                    type="button"
                    @click="previousPage"
                >
                    &lt;Previous
                </button>
            </span>
            <span>
                Page <b>{{ page }}</b> of <b>{{ pages.length + 1 }}</b>. Total <b>{{ total }}</b> records
            </span>
            <span class="page-item">
                <button
                    :disabled="page === pages.length + 1"
                    type="button"
                    class="nav-btn next"
                    @click="nextPage"
                >
                    Next&gt;
                </button>
            </span>
        </nav>
        <ApolloLoader :loading="$apollo.loading" />
        <table
            id="nodes-table"
            aria-label="Node list table"
        >
            <thead>
                <tr>
                    <th>Software</th>
                    <th>Name</th>
                    <th class="version-column">
                        Version
                    </th>
                    <th>Open signups</th>
                    <th>Total users</th>
                    <th>Active users half year</th>
                    <th>Active users monthly</th>
                    <th>Local posts</th>
                    <th>Local comments</th>
                    <th>Services</th>
                    <th>Country</th>
                </tr>
            </thead>
            <tbody>
                <NodesTableRow
                    v-for="edge in edges"
                    :key="edge.node.id"
                    :node="edge.node"
                    :stats="statsForNode(edge.node.id)"
                />
            </tbody>
        </table>
    </div>
</template>

<script>
import gql from 'graphql-tag'
import NodesTableRow from "./NodesTableRow"
import ApolloLoader from "./common/ApolloLoader"

const query = gql`
    query NodesTable($platformName: String!, $protocolName: String!,
        $first: Int!, $after: String!, $last: Int!, $before: String!, $search: String!) {

        nodes(platform:$platformName, protocol:$protocolName,
            first: $first, after: $after, last: $last, before: $before, search: $search) {
            totalCount
            edges {
                node {
                    id
                    name
                    version
                    openSignups
                    host
                    platform {
                        name
                        icon
                    }
                    countryCode
                    countryFlag
                    countryName
                    services {
                        name
                    }
                }
            }
            pageInfo {
                hasNextPage
                hasPreviousPage
                startCursor
                endCursor
            }
        },
        statsGlobalToday(platform: $platformName, protocol: $protocolName) {
            usersTotal
            usersHalfYear
            usersMonthly
            localPosts
            localComments
        }

        statsNodes(platform: $platformName, protocol: $protocolName) {
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
                this.edges = data.nodes.edges
                this.total = data.nodes.totalCount
                this.pageInfo = data.nodes.pageInfo
                this.pages = Array(...{length: this.total / this.rows}).map(Number.call, Number)
                const stats = {}
                for (const o of data.statsNodes) {
                    stats[o.node.id] = o
                }
                this.stats = stats
                this.globalStats = data.statsGlobalToday || {}
            },
            variables() {
                return {
                    platformName: this.platform,
                    protocolName: this.protocol,
                    first: this.rows,
                    after: "",
                    before: "",
                    last: this.rows,
                    search: "",
                }
            },
        },
    },
    name: "NodesTable",
    components: {NodesTableRow, ApolloLoader},
    props: {
        platform: {
            type: String,
            default: () => "",
        },
        protocol: {
            type: String,
            default: () => "",
        },
    },
    data() {
        return {
            searchVal: "",
            stats: {},
            variables: {},
            edges: [],
            pages: [],
            page: 1,
            rows: 50,
            total: 0,
        }
    },
    mounted() {
        // eslint-disable-next-line no-undef
        makeSortable(document.getElementById("nodes-table"))
    },
    methods: {
        statsForNode(nodeId) {
            if (this.stats[nodeId] === undefined) {
                return {
                    usersTotal: 0,
                    usersHalfYear: 0,
                    usersMonthly: 0,
                    localPosts: 0,
                    localComments: 0,
                }
            }
            return this.stats[nodeId]
        },
        search() {
            this.variables.search = this.searchVal
            this.getPage(1)
        },
        nextPage() {
            this.variables = {
                first: this.rows,
                after: this.pageInfo.endCursor,
                before: "",
                last: this.rows,
                search: this.searchVal,
            }
            this.getPage(this.page + 1)
        },
        previousPage() {
            // I don't know why this works, if you have a better way (I bet you do) please do a PR
            this.variables = {
                first: this.rows * this.page,
                after: "",
                before: this.pageInfo.startCursor,
                last: this.rows,
                search: this.searchVal,
            }
            this.getPage(this.page - 1)
        },
        getPage(page) {
            this.page = page
            this.edges = []
            // Fetch more data and transform the original result
            this.$apollo.queries.queries.fetchMore({
                // New variables
                variables: this.variables,
                // Transform the previous result with new data
                updateQuery: (previousResult, {fetchMoreResult}) => {
                    this.pageInfo = fetchMoreResult.nodes.pageInfo
                    return fetchMoreResult
                },
            })
        },
    },
}
</script>

<style scoped>
    .version-column {
        max-width: 150px;
        overflow: hidden;
    }

    .search-box {
        display: flex;
        flex-direction: row;
    }
    .search-bar {
        flex-grow: 8;
    }

    .nav {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
    }
    .nav-btn {
        display: inline-block;
        cursor: pointer;
        width: 8em;
        padding-top: 1em;
        padding-bottom: 1em;
        background-color: #ddd;
    }
    .page-link {
        display: inline-block;
        width: 6em;
        padding: 1em;
        background-color: #eee;
        cursor: pointer;
    }
    .active {
        background-color: #fff;
    }
</style>
