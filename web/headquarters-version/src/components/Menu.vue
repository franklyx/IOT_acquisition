<template>
    <div class="menu-wapper">
        <div v-if="backEndMenu">
            <el-menu default-active="0" @open="handleOpen" @close="handleClose" :router="true" :uniqueOpened="true" :default-openeds="['1']">
                <el-menu-item index="/supervise/user"><i class="el-icon-menu"></i>用户</el-menu-item>
                <el-submenu index="0">
                    <template slot="title"><i class="el-icon-message"></i>组织</template>
                    <el-menu-item index="/supervise/company">公司</el-menu-item>
                    <el-menu-item index="/supervise/workshop">车间</el-menu-item>
                    <el-menu-item index="/supervise/productionLine">生产线</el-menu-item>
                    <el-menu-item index="/supervise/device">设备</el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
                <el-submenu index="1">
                    <template slot="title"><i class="el-icon-setting"></i>班组</template>
                    <el-menu-item index="/supervise/teamConfig">班组配置</el-menu-item>
                    <el-menu-item index="/supervise/shiftsConfig">班次配置</el-menu-item>
                </el-submenu>
                <el-submenu index="2">
                    <template slot="title"><i class="el-icon-setting"></i>配置</template>
                    <el-menu-item index="/supervise/devConfig">设备信息</el-menu-item>
                    <el-menu-item index="/supervise/dataSourceConfig" v-if="isFormStatus">数据源</el-menu-item>
                    <el-menu-item index="/supervise/staticResourceConfig">图片源</el-menu-item>
                </el-submenu>
            </el-menu>
        </div>
        <div class="submenu-waper" v-else>
            <!-- <el-menu :uniqueOpened="true" class="el-menu-vertical-demo" v-for="(work,indexw) in workshop" :key="work._id" @open="handleOpen" @close="handleClose" default-active="2">
                <el-submenu :index="String(indexw)">
                    <template slot="title">{{work.name}}</template>
                    <div v-for="(line,indexl) in work.product_line" :key="line._id">
                        <el-menu-item :index="'/index/'+(indexw)+'-'+(indexl)" v-if="line['equipment']['length'] == 0">{{line.name}} </el-menu-item>
                        <el-submenu :index="(indexw)+'-'+(indexl)" v-else>
                            <template slot="title">{{line.name}}</template>
                            <el-menu-item :index="'/index/'+(dev['_id'])" v-for="(dev,indexd) in line.equipment" :key="dev._id" class="devices-ul" @click="chlickPath('/index/'+(dev['_id']))">
                                <router-link :to="{path:'/index/'+(dev['_id'])}" tag="p">{{dev['name']}}</router-link>
                            </el-menu-item>
                        </el-submenu>
                    </div>
                </el-submenu>
            </el-menu> -->
            <!-- <el-menu  class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :default-active="$route.path" :default-openeds="['0', '0-0']"> -->
            <!-- :unique-opened="true" -->
            <el-menu class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :default-active="activeMenu" :data="activeMenu" :default-openeds="['0', '0-0']">
                <el-submenu :index="String(indexw)" v-for="(work,indexw) in workshop" :key="work._id">
                    <template slot="title">{{work.name}}</template>
                    <div v-for="(line,indexl) in work.product_line" :key="line._id">
                        <!-- <el-menu-item :index="String(indexw)+'-'+String(indexl)" v-if="line['equipment']['length'] == 0">{{line.name}} </el-menu-item> -->
                        <el-submenu :index="(indexw)+'-'+(indexl)">
                            <template slot="title">{{line.name}}</template>
                            <!-- <el-menu-item :index="'/index/'+(indexw)+'-'+(indexl)+'-'+(indexd)" v-for="(dev,indexd) in line.devices" :key="dev">{{dev['name']}}</el-menu-item> -->
                            <el-menu-item :index="'/index/'+(dev['_id'])" v-for="(dev,indexd) in line.equipment" :key="dev._id" class="devices-ul" @click="chlickPath('/index/'+(dev['_id']))">
                                <router-link :to="{path:'/index/'+(dev['_id'])}" tag="p">{{dev['name']}}</router-link>
                            </el-menu-item>
                        </el-submenu>
                    </div>
                </el-submenu>
            </el-menu>
        </div>
    </div>
</template>
<script>
import {
    getMenuList
} from '@/service/api'
import {
    mapGetters
} from 'vuex'
export default {
    props: ['backEndMenu', 'id'],
    data() {
        return {
            activeIndex: '',
            isuniqueOpened: true,
            router: true,
            workshop: [],
            activeMenu: '',
            devicesList: []
        }
    },
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        chlickPath(param) {
            console.log(param)
            this.activeIndex = param
        }
    },
    computed: {
        ...mapGetters(['getToken', 'getFactoryId', 'isFormStatus'])
    },
    updated() {
        this.activeMenu = this.$route.path
    },
    mounted() {
        if (!this.backEndMenu) {
            getMenuList({
                factory_id: this.getFactoryId
            }).then(res => {
                if (res.code === 200) {
                    this.workshop = res.data
                        // 进入index路由,默认显示的设备
                    for (let ws of res.data) {
                        for (let pl of ws.product_line) {
                            for (let eq of pl.equipment) {
                                if (eq['_id']) {
                                    this.devicesList.push(eq['_id'])
                                    this.$emit('defaultDeId', this.devicesList)
                                    return
                                }
                            }
                        }
                    }
                }
            })
        }
    }
}
</script>
<style lang="scss" scoped>
.menu-wapper {
    height: 100%;
    overflow-y: scroll;
    /*滚动条*/
    &::-webkit-scrollbar {
        width: 1px;
        height: 1px;
        background-color: #ccc;
    }
    /*定义滚动条轨道 内阴影+圆角*/
    &::-webkit-scrollbar-track {
        -webkit-box-shadow: inset 0 0 6px #fff;
        // border-radius: 10px;  
        background-color: #fff;
    }
    /*定义滑块 内阴影+圆角*/
    &::-webkit-scrollbar-thumb {
        // border-radius: 10px;  
        -webkit-box-shadow: inset 0 0 6px #fff;
        background-color: #999;
    }
}
.submenu-waper{
    padding-bottom: 50px;
}
.devices-ul {
    background-color: #e4e6ea;
}
</style>
