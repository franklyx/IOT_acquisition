<template>
    <div class="status">
        <el-row :gutter="20">
            <el-col :xs="24" :sm="24" :md="24" :lg="10">
                <div class="img-box" :style="{backgroundImage:'url(http://'+getBaseUrl+''+activeBg+')'}">
                </div>
            </el-col>
            <el-col :xs="24" :sm="24" :md="24" :lg="14">
                <div class="status-info">
                    <h2>采集时间 : {{realTimeInfo['Timestamp']}}</h2>
                    <el-card class="box-card">
                        <div slot="header">
                            <span class="title">基本信息</span>
                        </div>
                        <el-row :gutter="20">
                            <el-col :span="12" :xs="24">
                                <p>出厂编号：{{basicInfo['factory_number']}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>出厂日期：{{basicInfo['factory_time']}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>产品型号：{{basicInfo['product_number']}}</p>
                            </el-col>
                        </el-row>
                    </el-card>
                    <el-card class="box-card">
                        <div slot="header">
                            <span class="title">实时信息</span>
                        </div>
                        <el-row :gutter="20">
                            <el-col :span="12" :xs="24">
                                <p>出厂编号：{{realTimeInfo.ManufacturingCode}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>出厂日期：{{realTimeInfo.ManufacturingDate}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>产品型号：{{realTimeInfo.ProductModel}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>运行状态：{{realTimeInfo.State}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>启动/待机/工作：</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>输入电压相位：{{realTimeInfo.PhaseVoltageInput}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>输入线电流（A）：{{realTimeInfo.LineIin}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>输入线电压（V）：{{realTimeInfo.LineVin}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>输入相电流（A）：{{realTimeInfo.PhaseIinAB}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>输入相电压（V）：{{realTimeInfo.PhaseVinAB}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>输出功率（W）：{{realTimeInfo.OutputPower}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>输入功率（W）：{{realTimeInfo.InputPower}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>输出直流电压（V）：{{realTimeInfo.DCVout}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>输出直流电流（A）：{{realTimeInfo.DCIout}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>能效比：{{realTimeInfo.EfficiencyRatio}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>保护气体用量（m³）：{{realTimeInfo.GasFlow}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>一次测温（℃）：{{realTimeInfo.Temperature1}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>二次测温（℃）：{{realTimeInfo.Temperature2}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>过流报警：{{realTimeInfo.OCAlarm}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>过压报警：{{realTimeInfo.OVAlarm}}</p>
                            </el-col>
                            <el-col :span="12" :xs="24">
                                <p>报警代码：{{realTimeInfo.AlarmCode}}</p>
                            </el-col>
                        </el-row>
                    </el-card>
                </div>
            </el-col>
        </el-row>
    </div>
</template>
<script>
import {
    getRealtimeData,
    getProductInfo
} from '@/service/api'
import {
    mapGetters
} from 'vuex'

export default {
    props: ['basicInfo'],
    data() {
        return {
            status: {},
            realTimeInfo: {},
            activeBg: 'url("../assets/images/default_bg.jpg")'
        }
    },
    computed: {
        ...mapGetters(['getFactoryId', 'getBaseUrl'])
    },
    watch: {
        basicInfo() {
            this.initData()
            this.getProductInfoFn()
            console.print('实时信息watch触发')
        }
    },
    mounted() {
        setInterval(() => {
            console.print('实时信息ajax长轮询触发')
            this.initData()
        }, 15000)
    },
    methods: {
        initData(eId) {
            getRealtimeData({
                factory_number: this.basicInfo.factory_number
            }).then(ress => {
                if (ress.code === 200) {
                    this.realTimeInfo = JSON.parse(ress.data)
                }
            })
        },
        getProductInfoFn() {
            getProductInfo({
                factory_id: this.getFactoryId,
                prodoct_number: this.basicInfo.product_number
            }).then(res => {
                if (res.code === 200) {
                    this.activeBg = res.data.pic_url
                }
            })
        }
    }
}
</script>
<style scoped lang="scss">
.status {
    height: 100%;
    h2 {
        font-size: 18px;
    }
    p {
        line-height: 40px;
    }
    .box-card {
        margin-top: 20px;
    }
}

.img-box {
    height: 762px;
    border: 1px solid #ccc;
    // display: none;
    background: url('../../assets/images/default_bg.jpg');
    background-size: 90%;
    background-position:center center;
    background-repeat:no-repeat;
}

@media(max-width:769px) {
    .img-box {
        display: none;
    }
}
</style>
