<template>
    <tr>
        <td>
            <img
                :alt="node.platform.name"
                :title="node.platform.name"
                :src="imageSource"
            />
        </td>
        <td>
            <router-link
                :title="node.name"
                :to="nodeUrl"
            >
                {{ node.name }}
            </router-link>
        </td>
        <td>{{ node.version }}</td>
        <td>{{ openSignups }}</td>
        <td>{{ stats.usersTotal }}</td>
        <td>{{ stats.usersHalfYear }}</td>
        <td>{{ stats.usersMonthly }}</td>
        <td>{{ stats.localPosts }}</td>
        <td>{{ stats.localComments }}</td>
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
        nodeUrl() {
            return `/node/${this.node.host}`
        },
        openSignups() {
            return this.node.openSignups ? "Yes" : "No"
        },
    },
}
</script>

<style scoped>

</style>
