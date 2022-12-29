<template>
    <div style="background-color: white; padding: 10px;">
        <p>Redirecting...</p>
        <p>If this takes longer than a second it is possible the redirection failed</p>
    </div>
</template>
<script>
import gql from 'graphql-tag'

const query = gql`
query ResolveName($name: String!) {
    thefederation_platform(where: {name: {_eq: $name}}) {
        id
    }
}
`

export default {
    apollo: {
        thefederation_platform: {
            query,
            variables() {
                return {
                    name: this.$route.params.platformName,
                }
            },
            result({data}) {
                if (data.thefederation_platform && data.thefederation_platform.length === 1) {
                    this.$router.push(`/platform/${data.thefederation_platform[0].id}`)
                }
            },
        },
    },
    name: 'PlatformRedirector',
}
</script>
