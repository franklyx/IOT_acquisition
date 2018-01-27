export default {
    // 设置localStorage
    set: function(name, json) {
        localStorage.removeItem(name)
        localStorage.setItem(name, JSON.stringify(json))
    },
    // 获取localStorage
    getInfo: function(name) {
        var info = localStorage.getItem(name)
        return info ? JSON.parse(info) : null
    },
    // 是否登录
    isLogined: function(name) {
        var isExpired = localStorage.getItem(name)
        if (isExpired) {
            return isExpired
        } else {
            return false
        }
    }
}
