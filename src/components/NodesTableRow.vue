<template>
    <tr>
        <td>
            <!--<img alt="{{ node.network }}" title="{{ node.network }}" src="images/{{ node.network }}-16.png"/>-->
        </td>
        <!--<td><a title="{{ node.name }}" href="/node/{{ node.host }}">{{ node.name }}</a></td>-->
        <td>{{ node.name }}</td>
        <!--<td>{{ node.version }}</td>-->
        <!--<td>{{ node.registrations_open }}</td>-->
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
    props: ['node'],
}
</script>

<style scoped>

</style>
