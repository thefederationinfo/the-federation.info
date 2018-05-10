import Chart from 'chart.js'
import Tooltip from 'vue-directive-tooltip'
import Vue from 'vue'
import VueApollo from 'vue-apollo'
import VueChartkick from 'vue-chartkick'
import {ApolloClient} from 'apollo-client'
import {HttpLink} from 'apollo-link-http'
import {InMemoryCache} from 'apollo-cache-inmemory'
import 'vue-directive-tooltip/css/index.css'

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

Vue.use(Tooltip, {
    delay: 100,
    placement: 'left',
    triggers: ['hover'],
})
Vue.use(VueApollo)
Vue.use(VueChartkick, {adapter: Chart})

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    provide: apolloProvider.provide(),
    components: {App},
    template: '<App/>',
})
