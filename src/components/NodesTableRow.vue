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
        <!--<td>{{ node.total_users }}</td>-->
        <!--<td>{{ node.active_users_halfyear }}</td>-->
        <!--<td>{{ node.active_users_monthly }}</td>-->
        <!--<td>{{ node.local_posts }}</td>-->
        <!--<td>{{ node.local_comments }}</td>-->
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
