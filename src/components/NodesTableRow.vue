<template>
    <tr>
        <td>
            <img
                :alt="node.platform.name"
                :title="node.platform.name"
                :src="imageSource"
            >
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
        <!--<td>{{ node.services }}</td>-->
        <!--<td>-->
            <!--<div v-if="node.country">-->
                <!--<a href="http://countrycode.org/{{ node.country }}" target="_blank">-->
                    <!--<img src="flags/{{ node.country|lower }}.png">-->
                <!--</a>-->
            <!--</div>-->
            <!--<div v-else>-->
                <!--&nbsp;-->
            <!--</div>-->
        <!--</td>-->
    </tr>
</template>

<script>
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
        imageSource()  {
            return `./static/images/${this.node.platform.name}-16.png`
        },
        openSignups() {
            return this.node.openSignups ? "Yes" : "No"
        },
    },
}
</script>

<style scoped>

</style>
