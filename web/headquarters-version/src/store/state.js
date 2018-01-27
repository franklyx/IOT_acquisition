import storage from '@/util/storage'
export default {
    user: storage.getInfo('user') || {},
    default_factory: storage.getInfo('default_factory') || {},
    fromStatus: false
}
