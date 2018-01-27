<template>
    <div class="wapper" id="wapper">
        <div class="main-top">
            <Headers></Headers>
        </div>
        <div class="main-left" :class="isOpen ? 'showleft' : 'hideleft'">
            <Menus :id="factoryId" v-on:defaultDeId="defaultDeId"></Menus>
            <div class="menusIcon" @click="menuIsOpen">
                <h3>焊机设备信息化管理平台</h3>
                <i class="iconfont icon-santiaogang"></i>
            </div>
        </div>
        <div class="marin-right">
            <div class="right-waper">
                <div class="scrollInfo">
                    <marquee class="marquee" direction="up" scrollamount="1" loop @mouseout="start($event)" @mouseover="stop">
                    <p v-for="item in socketData" v-if="socketData.length !== 0">
                        <span>采集时间: {{item.Timestamp}}</span>  
                        <!-- <span>出厂编号：{{item.ManufacturingCode}}</span> -->
                        <span>设备: {{item.equipment_name}} │ {{item.workshop_name}} │ {{item.line_name}}</span>
                        <!-- <span>车间: {{item.workshop_name}}</span>
                        <span>生产线: {{item.line_name}}</span> -->
                        <!-- <span>出厂日期：{{item.ManufacturingDate}}</span> -->
                        <!-- <span>产品型号：{{item.ProductModel}}</span> -->
                        <!-- <span>运行状态：{{item.State}}</span> -->
                        <!-- 输入电压相位：{{item.PhaseVoltageInput}}
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
                        二次测温（℃）：{{item.Temperature2}}-->
                        <span>过流报警：{{item.OCAlarm}}</span>
                        <span>过压报警：{{item.OVAlarm}}</span>
                        <span>报警代码：{{item.AlarmCode}}</span>
                    </p>
                    <p v-else>暂时没有报警</p>
                    </marquee>
                </div>
                <transition enter-active-class="animated bounceInUp">
                    <keep-alive>
                        <router-view :key="$route.params.id"></router-view>
                    </keep-alive>
                </transition>
            </div>
        </div>
    </div>
</template>
<script>
import Headers from '@/components/Headers'
import Menus from '@/components/Menu'
import { mapGetters } from 'vuex'
export default {
    name: 'wapper',
    data() {
        return {
            msg: 'zhouxin',
            theme3: 'light',
            isOpen: false,
            showleft: false,
            socketData: [],
            screenWidth: ''
        }
    },
    methods: {
        resize() {
            if (document.body.clientWidth > 768) {
                this.isOpen = true
            } else {
                this.isOpen = false
            }
            window.onresize = (ev) => {
                if (document.body.clientWidth > 768) {
                    this.isOpen = true
                } else {
                    this.isOpen = false
                }
            }
        },
        menuIsOpen() {
            this.isOpen = !this.isOpen
        },
        start(event) {
            event.currentTarget.start()
        },
        stop(event) {
            event.currentTarget.stop()
        },
        initWebSocket() {
            const socketHost = this.getBaseUrl
            const websocket = new WebSocket(`ws://${socketHost}api/v1/join-socket`)
            websocket.onopen = (evt) => {
                websocket.send(this.getToken)
            }
            websocket.onerror = function(evt) {
                console.log('err')
            }
            websocket.onmessage = (evt) => {
                if (evt.data) {
                    // console.log('WebSocket data....', evt.data)
                    this.socketData.push(JSON.parse(evt.data))
                }
            }
            websocket.onclose = function(evt) {
                console.log('WebSocket close...')
            }
        },
        defaultDeId(data) {
            if (this.$route.path === '/index') {
                this.$router.push(`/index/${data[0]}`)
            }
        }
    },
    computed: {
        factoryId() {
            return this.$route.query.id
        },
        ...mapGetters(['getFactoryId', 'getToken', 'getBaseUrl'])
    },
    mounted() {
        this.initWebSocket()
        this.resize()
    },
    components: {
        Headers,
        Menus
    }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.scrollInfo {
    color: red;
    padding-bottom: 20px;
}
.marquee{
    height: 35px;
    p{
        line-height: 1.5;
        span{
            padding-right: 20px;
        }
    }
}
.hideleft{}
</style>
