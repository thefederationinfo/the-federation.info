<template>
    <div>
        <div class="search-box">
            <input
                v-model="searchVal"
                aria-label="search box"
                type="text"
                placeholder="Search node name"
                class="search-bar"
            >
            <button
                aria-label="Search Button"
                class="nav-btn"
                @click="$emit('search', searchVal)"
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
                    @click="$emit('prev-page')"
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
                    @click="$emit('next-page')"
                >
                    Next&gt;
                </button>
            </span>
        </nav>
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
import NodesTableRow from "./NodesTableRow"

export default {
    name: "NodesTable",
    components: {NodesTableRow},
    props: {
        edges: {
            type: Array,
            default: () => [],
        },
        stats: {
            type: Object,
            default: () => {},
        },
        pages: {
            type: Array,
            default: () => [1],
        },
        page: {
            type: Number,
            default: () => 1,
        },
        rows: {
            type: Number,
            default: () => 50,
        },
        total: {
            type: Number,
            default: () => 1,
        },
    },
    data() {
        return {
            searchVal: "",
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
