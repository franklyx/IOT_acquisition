import fetch from './fetch'

// 登录
export function login({ username, password }) {
    return fetch({
        url: 'api/v1/token',
        method: 'post',
        data: {
            username: username,
            password: password
        }
    })
}

// 更新token
export function upDateToken({ rf_token }) {
    return fetch({
        url: '/api/v1/rf-token',
        method: 'post',
        data: {
            rf_token: rf_token
        }
    })
}

// 获取所有一个公司所有的车间，生产线，设备，以及之间的关系结构
export function getMenuList({ factory_id }) {
    return fetch({
        url: `/api/v1/relate-tree/factory/${factory_id}`,
        method: 'get'
    })
}

// 获取设备基本信息
export function getEquipmentInfo({ factory_id, equipment_id }) {
    return fetch({
        url: `/api/v1/equipment/${factory_id}/${equipment_id}`,
        method: 'get'

    })
}

// 获取设备图片
export function getProductInfo({ factory_id, prodoct_number }) {
    return fetch({
        url: `/api/v1/product/${factory_id}/${prodoct_number}`,
        method: 'get'
    })
}

// 获取报警信息
export function alarmData({ factory_id, factory_number, page, per_page }) {
    return fetch({
        url: `/api/v1/alarm-data/${factory_id}/${factory_number}`,
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }

    })
}

// 获取当前设备最新的实时信息
export function getRealtimeData({ factory_number }) {
    return fetch({
        url: `/api/v1/realtime-data/${factory_number}`,
        method: 'get'

    })
}

// 获取设备警告信息
export function getAlarmData({ factory_id, equipment_id, page, per_page }) {
    return fetch({
        url: `/api/v1/alarm-data/${factory_id}/${equipment_id}`,
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }
    })
}

// 根据设备id获取班组列表
export function getEquipmentBelongGroup({ factory_id, equipment_id }) {
    return fetch({
        url: `/api/v1/equipment-belong-group/${factory_id}/${equipment_id} `,
        method: 'get'
    })
}

// 获取历史信息
export function getHistoryData({ factory_id, factory_number, group_id, start_time, end_time, search_field, equipment_id }) {
    return fetch({
        url: `/api/v1/history-data/${factory_id}/${factory_number}`,
        method: 'post',
        data: {
            group_id: group_id,
            start_time: start_time,
            end_time: end_time,
            search_field: search_field,
            equipment_id: equipment_id
        }
    })
}

// 获报表信息
export function getReportData({ factory_id, date, search_field, equipment_id }) {
    return fetch({
        url: `/api/v1/report-data/${factory_id}/${equipment_id}`,
        method: 'post',
        data: {
            date: date,
            search_field: search_field
        }
    })
}

/* 后端接口 */

// 获取所有工厂
export function getFactory({ page, per_page }) {
    return fetch({
        url: 'api/v1/list/factory',
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }
    })
}

// 添加工厂
export function addFactory({ name }) {
    return fetch({
        url: '/api/v1/factory/',
        method: 'post',
        data: {
            name: name
        }
    })
}

// 修改工厂
export function modifyFactory({ factory_id, name }) {
    return fetch({
        url: `/api/v1/factory/${factory_id}`,
        method: 'put',
        data: {
            name: name
        }
    })
}

// 删除工厂
export function deleteFactory({ factory_id }) {
    return fetch({
        url: `/api/v1/factory/${factory_id}`,
        method: 'delete'
    })
}

// 获取用户列表
export function getUserList({ page, per_page }) {
    return fetch({
        url: '/api/v1/list/user',
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }
    })
}

// 修改用户账号密码
export function modifyUserinform({ user_id, name, password }) {
    return fetch({
        url: `/api/v1/user-inform/${user_id}`,
        method: 'put',
        data: {
            name: name,
            password: password
        }
    })
}

// 添加用户
export function addUser({ name, role, password, factory_id }) {
    return fetch({
        url: '/api/v1/user/',
        method: 'post',
        data: {
            name: name,
            role: role,
            password: password,
            factory_id: factory_id
        }
    })
}

// 删除用户
export function deleteUser({ id }) {
    return fetch({
        url: `/api/v1/user/${id}`,
        method: 'delete'
    })
}

// 修改用户
export function modifyUser({ id, name, role, password, factory_id }) {
    return fetch({
        url: `/api/v1/user/${id}`,
        method: 'put',
        data: {
            name: name,
            role: role,
            password: password,
            factory_id: factory_id
        }
    })
}

// 获取工厂信息
export function getFactoryInfo({ id }) {
    return fetch({
        url: `/api/v1/factory/${id}`,
        method: 'get'
    })
}

// 根据工厂获取车间列表
export function getWorkShop({ id, page, per_page }) {
    return fetch({
        url: `/api/v1/list/work-shop/${id}`,
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }
    })
}

// 添加车间
export function addWorkShop({ id, name }) {
    return fetch({
        url: `/api/v1/work-shop/${id}/`,
        method: 'post',
        data: {
            name: name
        }
    })
}

// 修改车间
export function modifyWorkShop({ factory_id, workshop_id, name }) {
    return fetch({
        url: `/api/v1/work-shop/${factory_id}/${workshop_id}`,
        method: 'put',
        data: {
            name: name
        }
    })
}

// 删除车间
export function deleteWorkShop({ factory_id, workshop_id }) {
    return fetch({
        url: `/api/v1/work-shop/${factory_id}/${workshop_id}`,
        method: 'delete'
    })
}

// 根据工厂获取生产线列表
export function getLineUnderShop({ factory_id, workshop_id }) {
    return fetch({
        url: `/api/v1/list/line-under-shop/${factory_id}/${workshop_id}`,
        method: 'get'
    })
}

// 根据车间获取生产线列表
export function getProductLine({ id, page, per_page }) {
    return fetch({
        url: `/api/v1/list/product-line/${id}`,
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }
    })
}

// 添加生产线
export function addProductLine({ factory_id, name, workshop_id }) {
    return fetch({
        url: `/api/v1/product-line/${factory_id}/`,
        method: 'post',
        data: {
            name: name,
            workshop_id: workshop_id
        }
    })
}

// 修改生产线
export function modifyProLine({ factory_id, productline_id, name, workshop_id }) {
    return fetch({
        url: `/api/v1/product-line/${factory_id}/${productline_id}`,
        method: 'put',
        data: {
            name: name,
            workshop_id: workshop_id
        }
    })
}

// 删除神产线
export function deleteProLine({ factory_id, productline_id }) {
    return fetch({
        url: `/api/v1/product-line/${factory_id}/${productline_id}`,
        method: 'delete'
    })
}

// 根据工厂获取设备
export function getDevice({ factory_id, page, per_page }) {
    return fetch({
        url: `/api/v1/list/equipment/${factory_id}`,
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }
    })
}

// 添加工厂设备
export function addDevice({ factory_id, name, workshop_id, line_id, factory_number, factory_time, product_number }) {
    return fetch({
        url: `/api/v1/equipment/${factory_id}/`,
        method: 'post',
        data: {
            name: name,
            workshop_id: workshop_id,
            line_id: line_id,
            factory_number: factory_number,
            factory_time: factory_time,
            product_number: product_number
        }
    })
}

// 修改工厂设备
export function modifyDevice({ factory_id, equipment_id, name, workshop_id, line_id, factory_number, factory_time, product_number }) {
    return fetch({
        url: `/api/v1/equipment/${factory_id}/${equipment_id}`,
        method: 'put',
        data: {
            name: name,
            workshop_id: workshop_id,
            line_id: line_id,
            factory_number: factory_number,
            factory_time: factory_time,
            product_number: product_number
        }
    })
}

// 删除工厂设备
export function deleteDevice({ factory_id, equipment_id }) {
    return fetch({
        url: `/api/v1/equipment/${factory_id}/${equipment_id}`,
        method: 'delete'
    })
}

// 根据工厂获取班组
export function getWorkGroup({ factory_id, page, per_page }) {
    return fetch({
        url: `/api/v1/list/work-group/${factory_id}`,
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }
    })
}

// 添加班组
export function addWorkGroup({ factory_id, name, equipment_list }) {
    return fetch({
        url: `/api/v1/work-group/${factory_id}/`,
        method: 'post',
        data: {
            name: name,
            equipment_list: equipment_list
        }
    })
}

// 修改班组
export function modifyWorkGroup({ factory_id, group_id, name, equipment_list }) {
    return fetch({
        url: `/api/v1/work-group/${factory_id}/${group_id}`,
        method: 'put',
        data: {
            name: name,
            equipment_list: equipment_list
        }
    })
}

// 删除班组
export function deleteWorkGroup({ factory_id, group_id }) {
    return fetch({
        url: `/api/v1/work-group/${factory_id}/${group_id}`,
        method: 'delete'
    })
}

// 根据工厂获取班次
export function getWorkSchedule({ factory_id, page, per_page }) {
    return fetch({
        url: `/api/v1/list/work-schedule/${factory_id}`,
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }
    })
}

// 添加班次
export function addWorkSchedule({ factory_id, group_id, name, start_time, end_time }) {
    console.log(start_time, end_time)
    return fetch({
        url: `/api/v1/work-schedule/${factory_id}/`,
        method: 'post',
        data: {
            group_id: group_id,
            name: name,
            start_time: start_time,
            end_time: end_time
        }
    })
}

// 修改班次
export function modifyWorkSchedule({ factory_id, schedule_id, name, group_id, start_time, end_time }) {
    return fetch({
        url: `/api/v1/work-schedule/${factory_id}/${schedule_id}`,
        method: 'put',
        data: {
            name: name,
            group_id: group_id,
            start_time: start_time,
            end_time: end_time
        }
    })
}

// 删除班次
export function deleteWorkSchedule({ factory_id, schedule_id }) {
    return fetch({
        url: `/api/v1/work-schedule/${factory_id}/${schedule_id}`,
        method: 'delete'
    })
}

// 获取所有设备信息
// export function getProduct({ factory_id, name, product_number, pic_url }) {
//     return fetch({
//         url: `/api/v1/product/${factory_id}/`,
//         method: 'post',
//         data: { name: name, product_number: product_number, pic_url: pic_url }
//     })
// }

// 获取所有设备
export function getProductList({ factory_id, page, per_page }) {
    return fetch({
        url: `/api/v1/list/product/${factory_id}`,
        method: 'post',
        data: { page: page, per_page: per_page }
    })
}

// 添加所有设备
export function addProduct({ factory_id, name, product_number, pic_url }) {
    return fetch({
        url: `/api/v1/product/${factory_id}/`,
        method: 'post',
        data: { name: name, product_number: product_number, pic_url: pic_url }
    })
}

// 修改所有设备
export function modifyProduct({ factory_id, product_id, name, product_number, pic_url }) {
    return fetch({
        url: `/api/v1/product/${factory_id}/${product_id}`,
        method: 'put',
        data: { name: name, product_number: product_number, pic_url: pic_url }
    })
}

// 修改所有设备
export function deleteProduct({ factory_id, product_id }) {
    return fetch({
        url: `/api/v1/product/${factory_id}/${product_id}`,
        method: 'delete'
    })
}

// 获取所有图片
export function getPicUrl() {
    return fetch({
        url: '/api/v1/list/pic-url',
        method: 'get'
    })
}

// 删除图片
export function deletePicUrl({ file_name }) {
    return fetch({
        url: `/api/v1/delete-file/${file_name}`,
        method: 'delete'
    })
}

// 添加数据源
export function addSource({ name, user, passwd, host, port, topic, qos, retain, keepalive, status }) {
    return fetch({
        url: '/api/v1/source/',
        method: 'post',
        data: {
            name: name,
            user: user,
            passwd: passwd,
            host: host,
            port: port,
            topic: topic,
            qos: qos,
            retain: retain,
            keepalive: keepalive,
            status: status
        }
    })
}

// 获取数据源列表
export function getSourceList({ page, per_page }) {
    return fetch({
        url: '/api/v1/list/source',
        method: 'post',
        data: {
            page: page,
            per_page: per_page
        }
    })
}

// 修改数据源列表
export function modifySource({ source_id, name, user, passwd, host, port, topic, qos, retain, keepalive, status }) {
    return fetch({
        url: `/api/v1/source/${source_id}`,
        method: 'put',
        data: {
            name: name,
            user: user,
            passwd: passwd,
            host: host,
            port: port,
            topic: topic,
            qos: qos,
            retain: retain,
            keepalive: keepalive,
            status: status
        }
    })
}

// 删除数据源
export function deleteSource({ source_id }) {
    return fetch({
        url: `/api/v1/source/${source_id}`,
        method: 'delete'
    })
}

// 是否初始化工厂
export function sysInit() {
    return fetch({
        url: '/api/v1/sys_init',
        method: 'get'
    })
}

// 初始化用户
export function initAdmin({ username, password }) {
    return fetch({
        url: '/api/v1/init_admin',
        method: 'post',
        data: {
            username: username,
            password: password
        }
    })
}
