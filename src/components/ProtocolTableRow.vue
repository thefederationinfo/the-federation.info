<template>
    <tr>
        <th>
            <router-link
                :to="{name: 'protocol', params: {protocol: protocol.id}}"
            >
                {{ protocol.name }}
            </router-link>
        </th>
        <td class="nodes">
            <Number :number="protocol.thefederation_node_protocols_aggregate.aggregate.count" />
        </td>
        <td class="users">
            <div v-if="protocol.thefederation_stats[0].users_total">
                <Number
                    :number="protocol.thefederation_stats[0].users_total
                    "
                />
            </div>
        </td>
    </tr>
</template>

<script>
import Number from './common/Number'

export default {
    name: "ProtocolTableRow",
    components: {Number},
    props: {
        protocol: {
            type: Object,
            default: null,
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
