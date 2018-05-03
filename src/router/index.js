import Vue from 'vue'
import Router from 'vue-router'
import IndexPage from '@/components/IndexPage'
import NodesPage from '@/components/NodesPage'
import PlatformPage from '@/components/platform/PlatformPage'

Vue.use(Router)

export default new Router({
    mode: 'history',
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
        {
            path: '/:platform/',
            component: PlatformPage,
        }
    ],
})
