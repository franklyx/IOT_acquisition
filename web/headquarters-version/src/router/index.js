import Vue from 'vue'
import Router from 'vue-router'
import storage from '@/util/storage'
import NProgress from 'nprogress'

import Index from '@/page/Index'
import Login from '@/page/Login'
import Factory from '@/page/Factory'
import Page from '@/page/frontEnd/Page'
import Hello from '@/components/Hello'

import Supervise from '@/page/backEnd/Supervise'
import User from '@/page/backEnd/User'
import Company from '@/page/backEnd/Company'
import Workshop from '@/page/backEnd/Workshop'
import ProductionLine from '@/page/backEnd/ProductionLine'
import Device from '@/page/backEnd/Device'
import TeamConfig from '@/page/backEnd/TeamConfig'
import ShiftsConfig from '@/page/backEnd/ShiftsConfig'
import DevConfig from '@/page/backEnd/DevConfig'
import DataSourceConfig from '@/page/backEnd/DataSourceConfig'
import StaticResourceConfig from '@/page/backEnd/StaticResourceConfig'
import FacInIt from '@/page/FacInit'










V
...ue.use(Router)
    /* eslint-disable */
let router = new Router({
    routes: [
        { path: '/login', name: 'Login', component: Login, meta: { requireAuth: true } },
        { path: '*', redirect: '/index' },
        { path: '/factory', component: Factory },
        { path: '/hello', component: Hello },
        { path: '/facInIt', component: FacInIt, meta: { requireAuth: true } },
        // frontend router
        {
            path: '/index',
            component: Index,
            children: [
                { path: '/index/:id', component: Page }
            ]
        },
        // backend router
        {
            path: '/supervise',
            component: Supervise,
            children: [
                { path: 'user', component: User },
                { path: 'company', component: Company },
                { path: 'workshop', component: Workshop },
                { path: 'productionLine', component: ProductionLine },
                { path: 'device', component: Device },
                { path: 'teamConfig', component: TeamConfig },
                { path: 'shiftsConfig', component: ShiftsConfig },
                { path: 'devConfig', component: DevConfig },
                { path: 'dataSourceConfig', component: DataSourceConfig },
                { path: 'staticResourceConfig', component: StaticResourceConfig }
            ]
        }
        // requireAuth: true 不需要登录权限
    ]
})

router.beforeEach((to, from, next) => {
    NProgress.start()
    if (to.meta.requireAuth) {
        // console.log('no login storage auth')
        next()
    } else {
        // console.log('need login storage auth')
        const isLoginInfo = storage.isLogined('user')
        const roleInfo = storage.getInfo('user')
        if (isLoginInfo) {
            if(roleInfo.role === 0 && to.fullPath.indexOf('supervise') !== -1){
                next({path: '/'})
            }
            next()
        } else {
            next({path:'/login'})
        }

    }
})

router.afterEach(() => {
    NProgress.done()
})

export default router
