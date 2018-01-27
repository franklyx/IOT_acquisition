import * as types from './types'

export default {
    [types.SET_USER](state, obj) {
        state.user = obj
    },
    [types.SET_FACTORY_ID](state, obj) {
        state.default_factory = {
            factory_id: obj
        }
    }
}
