import * as types from './types'
import storage from '@/util/storage'
import { login, upDateToken } from '@/service/api'

export default {
    login({ commit, state }, obj) {
        const userName = obj.username.trim()
        const password = obj.password.trim()
        return new Promise((resolve, reject) => {
            login({ username: userName, password: password }).then((res) => {
                if (res.code === 201 && res.data !== '') {
                    storage.set('user', res.data)
                    commit(types.SET_USER, res.data)
                }
                resolve(res)
            }).catch(err => {
                reject(err)
            })
        })
    },
    loginOut({ commit, state }, obj) {
        return new Promise((resolve, reject) => {
            localStorage.clear()
            resolve()
        })
    },
    selectFactory({ commit, state }, obj) {
        return new Promise((resolve, reject) => {
            commit(types.SET_FACTORY_ID, obj)
            storage.set('default_factory', { factory_id: obj })
            resolve()
        })
    },
    upDateTokenFn({ commit, state }, obj) {
        return new Promise((resolve, reject) => {
            let upToken = storage.getInfo('user')
            upDateToken({rf_token: upToken.rf_token}).then(res => {
                if (res.data) {
                    upToken.token = res.data.token
                    storage.set('user', upToken)
                    commit(types.SET_USER, upToken)
                    resolve(res)
                }
            })
        })
    }
}
