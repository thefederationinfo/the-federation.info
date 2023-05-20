<template>
    <footer>
        <p>
            <router-link to="/info">
                About
            </router-link> -
            <a
                href="https://codeberg.org/thefederationinfo/the-federation.info"
                rel="noopener noreferrer"
                @click="trackEvent('source_code')"
            >
                Source code
            </a> -
            <a
                href="https://socialhome.network/u/thefederation/"
                rel="noopener noreferrer"
                @click="trackEvent('mastodon')"
            >
                Follow
            </a> -
            <router-link to="/info/#privacy-policy">
                Privacy Policy
            </router-link>
        </p>
    </footer>
</template>

<script>
import {trackEvent} from '../../tracker'

export default {
    name: "Footer",
    methods: {
        trackEvent,
    },
}
</script>
