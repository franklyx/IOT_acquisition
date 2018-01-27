import storage from '@/util/storage'
export default {
    user: storage.getInfo('user') || {},
    default_factory: storage.getInfo('default_factory') || {},
    fromStatus: true,
    baseUrl: '10.9.36.126:7000/'
    // baseUrl: window.location.hostname + ':' + window.location.port + '/'
}
