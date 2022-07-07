<template>
    <tr>
        <th>
            <router-link
                :to="{name: 'protocol', params: {protocol: protocol.name}}"
            >
                {{ protocol.name }}
            </router-link>
        </th>
        <td class="nodes">
            <Number :number="protocol.activeNodes" />
        </td>
        <td class="users">
            <div v-if="statsProtocolToday">
                <Number :number="statsProtocolToday.usersTotal" />
            </div>
        </td>
    </tr>
</template>

<script>
import gql from 'graphql-tag'
import Number from './common/Number'

const statsQuery = gql`
    query ProtocolStats($name: String!) {
        statsProtocolToday(name: $name) {
            usersTotal
        }
    }
`

export default {
    apollo: {
        statsProtocolToday: {
            query: statsQuery,
            variables() {
                return {
                    name: this.protocol.name,
                }
            },
        },
    },
    name: "ProtocolTableRow",
    components: {Number},
    props: {
        protocol: {
            type: Object,
            default: null,
        },
    },
    data() {
        return {
            statsProtocolToday: {},
        }
    },
}
</script>

<style scoped>
    .nodes,
    .users {
        text-align: right;
    }
</style>
