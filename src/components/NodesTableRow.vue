<template>
    <tr>
        <td>
            <img
                v-if="node.platform.name !== 'unknown'"
                :alt="node.platform.name"
                :title="node.platform.name"
                :src="imageSource"
            >
            <div v-else>&nbsp;</div>
        </td>
        <td>
            <router-link
                :title="node.name"
                :to="{name: 'node', params: {host: node.host}}"
            >
                {{ node.name }}
            </router-link>
        </td>
        <td>{{ node.version }}</td>
        <td>{{ openSignups }}</td>
        <td>{{ stats.usersTotal ? stats.usersTotal : '' }}</td>
        <td>{{ stats.usersHalfYear ? stats.usersHalfYear : '' }}</td>
        <td>{{ stats.usersMonthly ? stats.usersMonthly : '' }}</td>
        <td>{{ stats.localPosts ? stats.localPosts : '' }}</td>
        <td>{{ stats.localComments ? stats.localComments : '' }}</td>
        <td>
            <span
                v-tooltip="services"
                v-if="services"
            >
                {{ node.services.length }}
            </span>
        </td>
        <td>
            <div
                v-if="node.countryCode"
                :title="node.countryName"
            >
                {{ node.countryFlag }}
            </div>
            <div v-else>
                &nbsp;
            </div>
        </td>
    </tr>
</template>

<script>
import _ from "lodash/collection"

export default {
    name: "NodesTableRow",
    props: {
        node: {
            type: Object,
            default: null,
        },
        stats: {
            type: Object,
            default: null,
        },
    },
    computed: {
        imageSource() {
            return `/static/images/${this.node.platform.name}-16.png`
        },
        openSignups() {
            return this.node.openSignups ? "Yes" : "No"
        },
        services() {
            const services = []
            for (const o of this.node.services) {
                services.push(o.name)
            }
            return _.sortBy(services).join(', ')
        },
    },
}
</script>
