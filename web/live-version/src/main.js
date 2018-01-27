// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
// import iview from 'iview'
// import 'iview/dist/styles/iview.css'
import 'animate.css'
import 'element-ui/lib/theme-default/index.css'
import '@/assets/css/reset.scss'
import '@/assets/iconfont/iconfont.css'
import 'nprogress/nprogress.css'
import store from './store'
import ElementUI from 'element-ui'
import infiniteScroll from 'vue-infinite-scroll'
import '@/util/console'

// Vue.use(iview)
Vue.use(ElementUI)
Vue.use(infiniteScroll)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    template: '<App/>',
    components: { App }
})
