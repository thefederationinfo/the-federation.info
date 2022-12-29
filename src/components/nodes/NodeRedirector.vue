<template>
    <div style="background-color: white; padding: 10px;">
        <p>Redirecting...</p>
        <p>If this takes longer than a second it is possible the redirection failed</p>
    </div>
</template>
<script>
import gql from 'graphql-tag'

const query = gql`
query ResolveHost($host: String!) {
    thefederation_node(where: {host: {_eq: $host}}) {
        id
    }
}
`

export default {
    apollo: {
        thefederation_node: {
            query,
            variables() {
                return {
                    host: this.$route.params.host,
                }
            },
            result({data}) {
                if (data.thefederation_node && data.thefederation_node.length === 1) {
                    this.$router.push(`/node/details/${data.thefederation_node[0].id}`)
                }
            },
        },
    },
    name: 'NodeRedirector',
}
</script>
