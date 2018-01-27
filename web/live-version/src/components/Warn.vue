<template>
    <div class="warn">
        <!-- <el-card class="box-card"> -->
        <!-- <div slot="header"> -->
        <el-input placeholder="输入关键词进行筛选" v-model="query"></el-input>
        <!-- </div> -->
        <div>
            <!-- <ul v-scroll="loadMore" v-infinite-scroll="loadMore" infinite-scroll-disabled="busy" infinite-scroll-distance="10"> -->
            <h2 class="list-title" v-if="filteredUntreated[0]">出厂编号：{{filteredUntreated[0]['ManufacturingCode']}}</h2>
            <div>
                <el-row :gutter="10">
                  <el-col :xs="8" :sm="6" :md="4" :lg="8">产品型号：{{filteredUntreated[0]['ProductModel']}}</el-col>
                  <el-col :xs="4" :sm="6" :md="8" :lg="8">出厂编号：{{filteredUntreated[0]['ManufacturingCode']}}</el-col>
                  <el-col :xs="4" :sm="6" :md="8" :lg="8">出厂日期：{{filteredUntreated[0]['ManufacturingDate']}}</el-col>
                </el-row>
            </div>
            <ul class="warn-content" ref="warnContent">
                <li v-infinite-scroll="loadMore" infinite-scroll-disabled="scrollDisable" infinite-scroll-distance="10">
                    <p v-for="(item,index) in filteredUntreated" :key="item.name" :style="{color:'red'}">
                        <el-row>
                            <el-col :span="6" :md="12" :lg="5" :xs="24" :sm="12">
                                采集时间1: {{item.Timestamp}}
                            </el-col>
                            <!-- <el-col :span="6" :md="12" :lg="5" :xs="24" :sm="12">
                                出厂编号：{{item.ManufacturingCode}}
                            </el-col> -->
                            <el-col :span="6" :md="12" :lg="3" :xs="24" :sm="12">
                                运行状态：{{item.State}}
                            </el-col>
                            <el-col :span="6" :md="12" :lg="3" :xs="24" :sm="12">
                                过流报警：{{item.OCAlarm}}
                            </el-col>
                            <el-col :span="6" :md="12" :lg="3" :xs="24" :sm="12">
                                过压报警：{{item.OVAlarm}}
                            </el-col>
                            <el-col :span="6" :md="12" :lg="5" :xs="24" :sm="12">
                                报警代码：{{item.AlarmCode}}
                            </el-col>
                        </el-row>
                    </p>
                    <p v-for="(item,index) in filteredHasBeen" :key="item.name">
                        <!-- 采集时间: {{item.Timestamp}} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;出厂编号：{{item.ManufacturingCode}} &nbsp;&nbsp;&nbsp;   产品型号：{{item.ProductModel}} 运行状态：{{item.State}} 启动/待机/工作：&nbsp;&nbsp;&nbsp;输入电压相位：{{item.PhaseVoltageInput}} 出厂日期：{{item.ManufacturingDate}}
                                输入线电流（A）：{{item.LineIin}}
                                输入线电压（V）：{{item.LineVin}}
                                输入相电流（A）：{{item.PhaseIinAB}}
                                输入相电压（V）：{{item.PhaseVinAB}}
                                输出功率（W）：{{item.OutputPower}}
                                输入功率（W）：{{item.InputPower}}
                                输出直流电压（V）：{{item.DCVout}}
                                输出直流电流（A）：{{item.DCIout}}
                                能效比：{{item.EfficiencyRatio}}
                                保护气体用量（m³）：{{item.GasFlow}} 
                                一次测温（℃）：{{item.Temperature1}}
                                二次测温（℃）：{{item.Temperature2}}
                                过流报警：{{item.OCAlarm}}&nbsp;&nbsp;&nbsp;
                                过压报警：{{item.OVAlarm}}&nbsp;&nbsp;&nbsp;
                                报警代码：{{item.AlarmCode}}-->
                        <el-row>
                            <el-col :span="6" :md="12" :lg="5" :xs="24" :sm="12">
                                采集时间: {{item.Timestamp}}
                            </el-col>
                            <!-- <el-col :span="6" :md="12" :lg="5" :xs="24" :sm="12">
                                出厂编号：{{item.ManufacturingCode}}
                            </el-col> -->
                            <el-col :span="6" :md="12" :lg="3" :xs="24" :sm="12">
                                运行状态：{{item.State}}
                            </el-col>
                            <el-col :span="6" :md="12" :lg="3" :xs="24" :sm="12">
                                过流报警：{{item.OCAlarm}}
                            </el-col>
                            <el-col :span="6" :md="12" :lg="3" :xs="24" :sm="12">
                                过压报警：{{item.OVAlarm}}
                            </el-col>
                            <el-col :span="6" :md="12" :lg="5" :xs="24" :sm="12">
                                报警代码：{{item.AlarmCode}}
                            </el-col>
                        </el-row>
                    </p>
                    <a class="more" href="javascript:;" v-loading="loading2">加载更多</a>
                </li>
            </ul>
        </div>
        <!-- </el-card> -->
    </div>
</template>
<script>
import {
    alarmData
} from '@/service/api'
import {
    mapGetters
} from 'vuex'

export default {
    props: ['basicInfo'],
    data() {
        return {
            query: '',
            data: [],
            hasBeen: [],
            untreated: [],
            factory_number: '',
            scrollDisable: false,
            page: 0,
            loading2: false
        }
    },
    watch: {
        basicInfo: {
            handler: 'getData'
                // deep: true
        }
    },
    computed: {
        filteredHasBeen() {
            var query = this.query && this.query.toLowerCase()
            var data = this.hasBeen
            if (query) {
                data = data.filter(function(row) {
                    return Object.keys(row).some(function(key) {
                        return String(row[key]).toLowerCase().indexOf(query) > -1
                    })
                })
            }
            return data
        },
        filteredUntreated() {
            var query = this.query && this.query.toLowerCase()
            var data = this.untreated
            if (query) {
                data = data.filter(function(row) {
                    return Object.keys(row).some(function(key) {
                        return String(row[key]).toLowerCase().indexOf(query) > -1
                    })
                })
            }
            return data
        },
        ...mapGetters(['getFactoryId'])
    },
    methods: {
        getData() {
            alarmData({
                factory_id: this.getFactoryId,
                factory_number: this.basicInfo.factory_number,
                page: this.page,
                per_page: 10
            }).then((ress) => {
                if (ress.code === 201) {
                    this.hasBeen = ress.data.has_been
                    this.untreated = ress.data.untreated
                }
            })
        },
        loadMore() {
            this.scrollDisable = true;
            this.loading2 = true;
            this.page += 1
            alarmData({
                factory_id: this.getFactoryId,
                factory_number: this.basicInfo.factory_number,
                page: this.page,
                per_page: 10
            }).then((ress) => {
                this.loading2 = false
                if (ress.code === 201) {
                    var has = ress.data.has_been
                    var unt = ress.data.untreated
                    if (has && has !== null) {
                        for (let i = 0, len = has.length; i < len; i++) {
                            this.hasBeen.push(has[i])
                        }
                    }
                    if (unt && unt !== null) {
                        for (let i = 0, len = unt.length; i < len; i++) {
                            this.untreated.push(unt[i])
                        }
                    }
                    this.scrollDisable = false
                    this.loading2 = false;
                }
            })
        }
    },
    mounted() {
        // this.getData()
    }
}
</script>
<style scoped lang="scss">
p {
    line-height: 30px;
}

.isState {
    color: red;
}

.el-row {
    margin-bottom: 20px;
}

.warn-content {
    padding: 20px;
    overflow-y: scroll;
    overflow: auto;
    max-height: 600px;
}
.more{
    text-align: center;
    display: block;
    color: #ccc;
    height: 50px;
}
.list-title{
    padding:10px 0 0 20px;
    font-weight: blod;
}
</style>
