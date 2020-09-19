<template>
    <tr>
        <td style="width: 20px;">
            <img
                v-if="platform.name !== 'unknown' && platform.icon !== 'unknown'"
                :alt="platform.name"
                :title="platform.name"
                :src="imageSource"
            >
            <div v-else>
&nbsp;
            </div>
        </td>
        <th style="text-align: left;">
            <router-link
                :to="{name: 'platform', params: {platform: platform.name}}"
            >
                {{ platform.displayName ? platform.displayName : platform.name }}
            </router-link>
        </th>
        <td class="nodes">
            <Number :number="nodeCount" />
        </td>
        <td class="users">
            <div v-if="statsPlatformToday">
                <Number :number="statsPlatformToday.usersTotal" />
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
import gql from 'graphql-tag'
import Number from './common/Number'


const platformStatsQuery = gql`
    query PlatformStats($name: String!) {
        statsPlatformToday(name: $name) {
            usersTotal
        }
    }
`

export default {
    apollo: {
        statsPlatformToday: {
            query: platformStatsQuery,
            variables() {
                return {
                    name: this.platform.name,
                }
            },
        },
    },
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
        nodeCount() {
            return this.platform.nodes.length
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
