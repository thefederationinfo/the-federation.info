import Vue from 'vue'
import Router from 'vue-router'

import IndexPage from '@/components/IndexPage'
import InfoPage from '@/components/InfoPage'
import NodePage from '@/components/nodes/NodePage'
import NodeRedirector from '@/components/nodes/NodeRedirector'
import NodesPage from '@/components/NodesPage'
import PlatformPage from '@/components/platform/PlatformPage'
import PlatformRedirector from '@/components/platform/PlatformRedirector'
import ProtocolPage from '@/components/protocols/ProtocolPage'
import HostingReport from "../components/HostingReportPage"

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: '/',
    routes: [
        {
            path: '/hostingreport',
            component: HostingReport,
            name: 'hostingreport',
        },
        {
            path: '/',
            component: IndexPage,
            name: 'index',
        },
        {
            path: '/nodes',
            component: NodesPage,
            name: 'nodes',
        },
        {
            path: '/node/:host',
            component: NodeRedirector,
            name: 'nodeRedirector',
        },
        {
            path: '/node/details/:id',
            component: NodePage,
            name: 'node',
        },
        {
            path: '/protocol/:protocol',
            component: ProtocolPage,
            name: 'protocol',
        },
        {
            path: '/info',
            component: InfoPage,
            name: 'info',
        },
        {
            path: '/platform/:platform',
            component: PlatformPage,
            name: 'platform',
        },
        {
            path: '/:platformName',
            component: PlatformRedirector,
            name: 'platformRedirector',
        },
    ],
    scrollBehavior(to, from, savedPosition) {
        if (to.hash) {
            return {selector: to.hash}
        } if (savedPosition) {
            return savedPosition
        }
        return {x: 0, y: 0}
    },
})
