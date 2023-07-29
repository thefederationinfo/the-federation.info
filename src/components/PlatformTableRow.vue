<template>
    <tr>
        <td style="width: 20px;">
            <img
                v-if="platform.name !== 'unknown' && platform.icon !== 'unknown'"
                :alt="platform.name"
                :title="platform.name"
                :src="imageSource"
                style="max-width: 1em;"
            >
            <div v-else>
&nbsp;
            </div>
        </td>
        <th style="text-align: left;">
            <router-link
                :to="{name: 'platform', params: {platform: platform.id}}"
            >
                {{ platform.display_name ? platform.display_name : platform.name }}
            </router-link>
        </th>
        <td class="nodes">
            <Number :number="platform.thefederation_nodes_aggregate.aggregate.count" />
        </td>
        <td class="users">
            <div v-if="statsPlatformToday">
                <Number :number="platform.thefederation_stats[0].users_total" />
            </div>
        </td>
        <td>
            <a
                v-if="platform.website"
                :href="platform.website"
                target="_blank"
                rel="noopener noreferrer"
            >
                {{ websiteWithoutProtocol }}
            </a>
        </td>
        <td>
            <a
                v-if="platform.code && platform.license"
                :href="platform.code"
                target="_blank"
                rel="noopener noreferrer"
            >
                {{ platform.license }}
            </a>
        </td>
    </tr>
</template>

<script>
import Number from './common/Number'

export default {
    name: "PlatformTableRow",
    components: {Number},
    props: {
        platform: {
            type: Object,
            default: null,
        },
    },
    data() {
        return {
            statsPlatformToday: {},
        }
    },
    computed: {
        imageSource() {
            return `/static/images/${this.platform.icon}-16.png`
        },
        websiteWithoutProtocol() {
            return this.platform.website.replace('https://', '').replace('http://', '')
        },
    },
}
</script>

<style scoped>
    .nodes,
    .users {
        text-align: right;
    }
</style>
