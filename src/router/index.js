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
import track from "../tracker"

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: '/',
    routes: [
        {
            path: '/hostingreport',
            component: HostingReport,
            name: 'hostingreport',
            beforeEnter(to, from, next) {
                track('/hostingreport')
                next()
            },
        },
        {
            path: '/',
            component: IndexPage,
            name: 'index',
            beforeEnter(to, from, next) {
                track(to.fullPath)
                next()
            },
        },
        {
            path: '/nodes',
            component: NodesPage,
            name: 'nodes',
            beforeEnter(to, from, next) {
                track('/nodes')
                next()
            },
        },
        {
            path: '/node/:host',
            component: NodeRedirector,
            name: 'nodeRedirector',
            beforeEnter(to, from, next) {
                track('/node/*')
                next()
            },
        },
        {
            path: '/node/details/:id',
            component: NodePage,
            name: 'node',
            beforeEnter(to, from, next) {
                track('/node/details/*')
                next()
            },
        },
        {
            path: '/protocol/:protocol',
            component: ProtocolPage,
            name: 'protocol',
            beforeEnter(to, from, next) {
                track('/protocol/*')
                next()
            },
        },
        {
            path: '/info',
            component: InfoPage,
            name: 'info',
            beforeEnter(to, from, next) {
                track('/info')
                next()
            },
        },
        {
            path: '/platform/:platform',
            component: PlatformPage,
            name: 'platform',
            beforeEnter(to, from, next) {
                track('/platform/*')
                next()
            },
        },
        {
            path: '/:platformName',
            component: PlatformRedirector,
            name: 'platformRedirector',
            beforeEnter(to, from, next) {
                track('/*')
                next()
            },
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
