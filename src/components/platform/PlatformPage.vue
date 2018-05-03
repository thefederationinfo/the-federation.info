<template>
    <div>
        <Drawer />
        <main>
            <header class="main-header">
                <div class="main-title">
                    <h1>{{ title }}</h1>
                    <h2 v-if="platform">{{ platform.tagline }}</h2>
                </div>
                <div class="flex">
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            0 <strong>Nodes</strong>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            0 <strong>Users</strong>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            0 <strong>Posts</strong>
                        </div>
                    </div>
                    <div class="col4">
                        <div class="tile valign-wrapper">
                            0 <strong>Comments</strong>
                        </div>
                    </div>
                </div>
            </header>
            <section class="tile">
                <header>
                    <h2>What is {{ title }}?</h2>
                </header>
                <div>
                    <div class="flex">
                        <div class="col2">
                            <p v-if="platform">{{ platform.description }}</p>
                            <div class="flex">
                                <div class="col2 center">
                                    <a
                                        v-if="platform"
                                        :href="platform.website"
                                        class="btn btn-primary"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        Official website
                                    </a>
                                </div>
                                <div class="col2 center">
                                    <a
                                        v-if="platform"
                                        :href="platform.code"
                                        class="btn"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        Source code
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="col2">
                            <ul>
                                <li>Nodes: <strong>0</strong></li>
                                <li>Users: <strong>0</strong></li>
                                <li>Last 6 months users: <strong>0</strong></li>
                                <li>Last month users: <strong>0</strong></li>
                                <li>Posts: <strong>0</strong></li>
                                <li>Comments: <strong>0</strong></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>
            <!--charts -->
            <section class="tile">
                <header>
                    <h2>All {{ title }} nodes</h2>
                </header>
                <div class="overflow-x">
                    <!-- nodes table -->
                </div>
            </section>
        </main>
        <Footer />
    </div>
</template>

<script>
import gql from 'graphql-tag'

import Drawer from "../common/Drawer"
import Footer from "../common/Footer"

const query = gql`
    query Platform($name: String!) {
        platforms(name: $name) {
            name
            displayName
            description
            website
        }
    }
`

export default {
    apollo: {
        queries: {
            query,
            manual: true,
            result({data}) {
                this.platform = data.platforms[0]
            },
            variables() {
                return {
                    name: this.$route.params.platform,
                }
            },
        },
    },
    name: 'PlatformPage',
    components: {Footer, Drawer},
    data() {
        return {
            platform: {},
        }
    },
    computed: {
        title() {
            if (this.platform === undefined) {
                return ''
            }
            return this.platform.displayName ? this.platform.displayName : this.platform.name
        },
    },
}
</script>

<style scoped>

</style>
