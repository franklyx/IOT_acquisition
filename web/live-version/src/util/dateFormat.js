export const dateFormat = function(_date) {
    let date = new Date(_date)
    let date_value = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
    return date_value
}
export const mouthFormat = function(_date) {
    let date = new Date(_date)
    let date_value = date.getFullYear() + '-' + (date.getMonth() + 1)
    return date_value
}
export const timeFormat = function(_date) {
    let date = new Date(_date)
    let date_value = date.getHours() + ':' + date.getMinutes()
    return date_value
}
export const dateTimeFormat = function(_date) {
    let date = new Date(_date)
    let date_value = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds()
    return date_value
}
