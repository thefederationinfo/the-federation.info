<template>
    <tr>
        <td>
            <PlatformIcon
                v-if="node.thefederation_platform.name !== 'unknown'"
                :name="node.thefederation_platform.name"
            />
            <div v-else>
&nbsp;
            </div>
        </td>
        <td>
            <router-link
                :title="node.name"
                :to="{name: 'node', params: {id: node.id}}"
            >
                {{ node.name }}
            </router-link>
        </td>
        <td class="version-column">
            {{ node.version }}
        </td>
        <td>{{ openSignups }}</td>
        <td>{{ stats.users_total ? Math.ceil(stats.users_total) : '-' }}</td>
        <td>{{ stats.users_half_year ? Math.ceil(stats.users_half_year) : '-' }}</td>
        <td>{{ stats.users_monthly ? Math.ceil(stats.users_monthly) : '-' }}</td>
        <td>{{ stats.local_posts ? Math.ceil(stats.local_posts) : '-' }}</td>
        <td>{{ stats.local_comments ? Math.ceil(stats.local_comments) : '-' }}</td>
        <td>
            <span
                v-if="services"
                v-tooltip="services"
            >
                {{ node.thefederation_node_services.length }}
            </span>
            <span v-else>-</span>
        </td>
        <td>
            <div
                v-if="node.country"
                :title="node.country"
            >
                {{ resolveCountryFlag }}
            </div>
            <div v-else>
                &nbsp;
            </div>
        </td>
    </tr>
</template>

<script>
import _ from "lodash/collection"
import getUnicodeFlagIcon from 'country-flag-icons/unicode'

import PlatformIcon from './common/PlatformIcon'

export default {
    name: "NodesTableRow",
    components: {PlatformIcon},
    props: {
        node: {
            type: Object,
            default: null,
        },
    },
    data() {
        return {
            stats: this.node.thefederation_stats_aggregate.aggregate.avg,
        }
    },
    computed: {
        openSignups() {
            return this.node.open_signups ? "Yes" : "No"
        },
        services() {
            const services = []
            for (const o of this.node.thefederation_node_services) {
                services.push(o.thefederation_service.name)
            }
            return _.sortBy(services).join(', ')
        },
        resolveCountryFlag() {
            return getUnicodeFlagIcon(this.node.country)
        },
    },
}
</script>

<style scoped>
    .version-column {
        max-width: 150px;
        overflow: hidden;
    }
</style>
