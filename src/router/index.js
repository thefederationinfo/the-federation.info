import Vue from 'vue'
import Router from 'vue-router'
import IndexPage from '@/components/IndexPage'
import NodesPage from '@/components/NodesPage'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'index',
            component: IndexPage,
        },
        {
            path: '/nodes',
            name: 'nodes',
            component: NodesPage,
        },
    ],
})
