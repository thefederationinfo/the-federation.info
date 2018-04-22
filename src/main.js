import Vue from 'vue'
import VueApollo from 'vue-apollo'
import { ApolloClient } from 'apollo-client'
import { HttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'

import App from './App'
import router from './router'

const httpLink = new HttpLink({
    uri: process.env.API_URI,
    useGETForQueries: true,
    headers: {
        'Content-Type': 'application/graphql',
    },
})

const apolloClient = new ApolloClient({
    link: httpLink,
    cache: new InMemoryCache(),
})

const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
})

Vue.use(VueApollo)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    provide: apolloProvider.provide(),
    components: {App},
    template: '<App/>',
})
