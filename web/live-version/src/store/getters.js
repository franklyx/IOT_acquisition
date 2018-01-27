export default {
    getUserName: state => state.user.username,
    getUserId: state => state.user.user_id,
    getRole: state => state.user.role,
    getToken: state => state.user.token,
    getFactoryId: state => state.user.factory_id,
    isFormStatus: state => state.fromStatus,
    getBaseUrl: state => state.baseUrl
}
