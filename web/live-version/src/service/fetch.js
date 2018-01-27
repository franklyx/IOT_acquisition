import axios from 'axios'
import store from '@/store'
import router from '@/router'
// import { Notification, Message } from 'element-ui'
import { Message } from 'element-ui'

const service = axios.create({
    baseURL: 'http://10.9.36.126:7000',
    headers: { 'Content-Type': 'application/json' }
})

// requset请求拦截
service.interceptors.request.use((config) => {
    if (store.getters.getToken) {
        config.headers['token'] = `${store.getters.getToken}`
    }
    return config
}, (error) => {
    return Promise.reject(error)
})

// response请求拦截
service.interceptors.response.use((response) => {
    const msg = response.data.msg
    if (msg !== 'success') {
        // Notification({
        //     title: response.data.msg,
        //     type: 'warning',
        //     message: `错误信息: ${msg} 错误url: ${response.config.url}`,
        //     offset: 100,
        //     duration: 1000 * 2
        // })
    }
    // token过期或错误
    if (msg === 'Wrong token.' || msg === 'Messing token.') {
        Message({
            message: 'token过期',
            type: 'error',
            duration: 5 * 1000
        })
        store.dispatch('upDateTokenFn').then(res => {
            router.go(0)
        })
    }
    // rf-token过期
    if (msg === 'Wrong rf-token.') {
        router.push('/login')
    }
    return response.data
}, (error) => {
    return Promise.reject(error)
})

export default service
