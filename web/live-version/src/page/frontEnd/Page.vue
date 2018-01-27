<template>
    <div>
        <el-tabs type="border-card" v-model="activeName" @tab-click="selectTabs">
            <el-tab-pane label="设备状态" name="status">
                <Status :basicInfo="equipmentInfo"></Status>
            </el-tab-pane>
            <el-tab-pane label="设备警告" name="warn">
                <Warn v-if="WarnShow" :basicInfo="equipmentInfo"></Warn>
            </el-tab-pane>
            <el-tab-pane label="历史查询" name="history">
                <History v-if="historyShow" :equipmentId="$route.path.split('/')[2]" :factoryId="getFactoryId" :basicInfo="equipmentInfo"></History>
            </el-tab-pane>
            <el-tab-pane label="报表系统" name="tab">
                <Tab v-if="TabShow" :equipmentId="$route.path.split('/')[2]" :factoryId="getFactoryId" :basicInfo="equipmentInfo"></Tab>
            </el-tab-pane>
            <el-tab-pane label="设备档案" name="shebei">设备档案</el-tab-pane>
        </el-tabs>
    </div>
</template>
<script>
// import Status from '@/components/Status'
// import Warn from '@/components/Warn'
// import Tab from '@/components/Tab'
// import History from '@/components/History'
import {
    mapGetters
} from 'vuex'
import {
    getEquipmentInfo
} from '@/service/api'
export default {
    computed: {
        ...mapGetters(['getFactoryId'])
    },
    methods: {
        selectTabs(tab, event) {
            // if (tab.name === 'history') {
            //     this.historyShow = true
            // }
            switch (tab.name) {
            case 'history':
                this.historyShow = true
                break;
            case 'warn':
                this.WarnShow = true
                break;
            case 'tab':
                this.TabShow = true
                break;
            default:
                break;
            }
        },
        getEquipmentFn(eId) {
            getEquipmentInfo({
                factory_id: this.getFactoryId,
                equipment_id: eId
            }).then(res => {
                if (res.code === 200) {
                    this.equipmentInfo = res.data
                }
            })
        }
    },
    data() {
        return {
            activeName: 'status',
            data: '',
            historyShow: false,
            TabShow: false,
            WarnShow: false,
            equipmentInfo: ''
        }
    },
    mounted() {
        this.getEquipmentFn(this.$route.path.split('/')[2])
    },
    components: {
        Status: () => System.import('@/page/frontEnd/Status'),
        Tab: () => System.import('@/page/frontEnd/Tab'),
        Warn: () => System.import('@/page/frontEnd/Warn'),
        History: () => System.import('@/page/frontEnd/History')
    }
}
</script>
<style scoped>
.el-tabs__item {
    padding: 10 20px!important;
}
</style>
