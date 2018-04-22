import Vue from 'vue'
import Router from 'vue-router'
import IndexPage from '@/components/IndexPage'
import NodesPage from '@/components/NodesPage'

Vue.use(Router)

export default new Router({
    mode: 'history',
    fallback: false,
    base: '/',
    routes: [
        {
            path: '/',
            component: IndexPage,
        },
        {
            path: '/nodes/',
            component: NodesPage,
        },
    ],
})
