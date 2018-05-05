import Vue from 'vue'
import Router from 'vue-router'

import IndexPage from '@/components/IndexPage'
import NodePage from '@/components/nodes/NodePage'
import NodesPage from '@/components/NodesPage'
import PlatformPage from '@/components/platform/PlatformPage'
import ProtocolPage from '@/components/protocols/ProtocolPage'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: '/',
    routes: [
        {
            path: '/',
            component: IndexPage,
            name: 'index',
        },
        {
            path: '/nodes/',
            component: NodesPage,
            name: 'nodes',
        },
        {
            path: '/node/:host',
            component: NodePage,
            name: 'node',
        },
        {
            path: '/protocol/:protocol',
            component: ProtocolPage,
            name: 'protocol',
        },
        {
            path: '/:platform/',
            component: PlatformPage,
            name: 'platform',
        },
    ],
})
