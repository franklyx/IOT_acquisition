# 焊机设备信息化管理平台

> 工厂版

## Build Setup

``` bash
# 安装依赖
npm install

# 开发环境启动服务
npm run dev

# 打包构建
npm run build

# 打包构建服务并查看性能分析
npm run build --report
```
## Libraries

- [Vuex](https://vuex.vuejs.org) : vuex全局状态管理
- [Vue-router](http://router.vuejs.org/) : vue路由
- [elementUI](http://element.eleme.io/#/zh-CN/component/installation) : elementUI框架
- [axios](https://github.com/mzabriskie/axios) : Ajax
- [vue-infinite-scroll](https://github.com/ElemeFE/vue-infinite-scroll) : 无限滚动加载
- [animate.css](https://daneden.github.io/animate.css/) :  动画库

## File Structure
```
    |-- .babelrc
    |-- .editorconfig
    |-- .eslintignore
    |-- .eslintrc.js
    |-- .gitignore
    |-- .postcssrc.js
    |-- favicon.ico
    |-- index.html
    |-- package.json
    |-- README.md
    |-- build
    |   |-- build.js
    |   |-- check-versions.js
    |   |-- dev-client.js
    |   |-- dev-server.js
    |   |-- utils.js
    |   |-- vue-loader.conf.js
    |   |-- webpack.base.conf.js
    |   |-- webpack.dev.conf.js
    |   |-- webpack.prod.conf.js
    |-- config
    |   |-- dev.env.js
    |   |-- index.js
    |   |-- prod.env.js
    |-- dist
    |   |-- index.html
    |   |-- static
    |       |-- favicon.ico
    |       |-- css
    |       |   |-- app.css
    |       |-- fonts
    |       |   |-- element-icons.b02bdc1.ttf
    |       |-- img
    |       |   |-- default_bg.afa11f5.jpg
    |       |   |-- proLogin.80e6c96.png
    |       |-- js
    |           |-- 0.js
    |           |-- 1.js
    |           |-- 2.js
    |           |-- 3.js
    |           |-- app.js
    |           |-- manifest.js
    |           |-- vendor.js
    |-- src
    |   |-- App.vue
    |   |-- main.js
    |   |-- assets
    |   |   |-- favicon.ico
    |   |   |-- logo.png
    |   |   |-- css
    |   |   |   |-- reset.scss
    |   |   |-- iconfont
    |   |   |   |-- demo.css
    |   |   |   |-- demo_fontclass.html
    |   |   |   |-- demo_symbol.html
    |   |   |   |-- demo_unicode.html
    |   |   |   |-- download.zip
    |   |   |   |-- iconfont.css
    |   |   |   |-- iconfont.eot
    |   |   |   |-- iconfont.js
    |   |   |   |-- iconfont.svg
    |   |   |   |-- iconfont.ttf
    |   |   |   |-- iconfont.woff
    |   |   |   |-- font_m06ioavhxgp3c8fr
    |   |   |       |-- demo.css
    |   |   |       |-- demo_fontclass.html
    |   |   |       |-- demo_symbol.html
    |   |   |       |-- demo_unicode.html
    |   |   |       |-- iconfont.css
    |   |   |       |-- iconfont.eot
    |   |   |       |-- iconfont.js
    |   |   |       |-- iconfont.svg
    |   |   |       |-- iconfont.ttf
    |   |   |       |-- iconfont.woff
    |   |   |-- images
    |   |   |   |-- default_bg.jpg
    |   |   |   |-- hj.png
    |   |   |   |-- proLogin.png
    |   |   |-- js
    |   |-- components
    |   |   |-- Headers.vue
    |   |   |-- Hello.vue
    |   |   |-- Menu.vue
    |   |-- page
    |   |   |-- FacInit.vue
    |   |   |-- Factory.vue
    |   |   |-- Index.vue
    |   |   |-- Login.vue
    |   |   |-- backEnd
    |   |   |   |-- Company.vue
    |   |   |   |-- DataSourceConfig.vue
    |   |   |   |-- DevConfig.vue
    |   |   |   |-- Device.vue
    |   |   |   |-- ProductionLine.vue
    |   |   |   |-- ShiftsConfig.vue
    |   |   |   |-- StaticResourceConfig.vue
    |   |   |   |-- Supervise.vue
    |   |   |   |-- TeamConfig.vue
    |   |   |   |-- User.vue
    |   |   |   |-- Workshop.vue
    |   |   |-- frontEnd
    |   |       |-- History.vue
    |   |       |-- Page.vue
    |   |       |-- Status.vue
    |   |       |-- Tab.vue
    |   |       |-- Warn.vue
    |   |-- router
    |   |   |-- index.js
    |   |-- service
    |   |   |-- api.js
    |   |   |-- fetch.js
    |   |-- store
    |   |   |-- actions.js
    |   |   |-- getters.js
    |   |   |-- index.js
    |   |   |-- mutations.js
    |   |   |-- state.js
    |   |   |-- types.js
    |   |-- util
    |       |-- console.js
    |       |-- dateFormat.js
    |       |-- storage.js
    |-- static
        |-- .gitkeep
        |-- favicon.ico

```