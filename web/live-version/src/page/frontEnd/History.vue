<template>
    <div>
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
            <el-form-item label="开始时间">
                <el-date-picker v-model="formInline.start_time" type="date" placeholder="选择日期时间"> </el-date-picker>
            </el-form-item>
            <el-form-item label="结束时间">
                <el-date-picker v-model="formInline.end_time" type="date" placeholder="选择日期时间"> </el-date-picker>
            </el-form-item>
            <el-form-item label="选择班组">
                <el-select v-model="formInline.optionsValue" placeholder="请选择">
                    <el-option v-for="item in formInline.options" :key="item._id" :label="item.name" :value="item._id">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="类型">
                <el-select v-model="formInline.typesValue" placeholder="请选择">
                    <el-option v-for="item in formInline.types" :key="item.value" :label="item.name" :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="drawPie">查询</el-button>
            </el-form-item>
        </el-form>
        <el-row>
            <el-col :xs="24" :sm="24" :md="24" :lg="24" id="main" :span="24">
                <!-- <div ></div> -->
            </el-col>
        </el-row>
    </div>
</template>
<script>
import {
    getEquipmentBelongGroup,
    getHistoryData
} from '@/service/api'
import {
    dateFormat
} from '@/util/dateFormat'
var echarts = require('echarts/lib/echarts')
require('echarts/lib/chart/line')
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
require('echarts/lib/component/toolbox')
require('echarts/lib/component/dataZoom')
export default {
    props: ['equipmentId', 'factoryId', 'basicInfo'],
    name: '',
    data() {
        return {
            formInline: {
                // start_time: 'Tue Aug 01 2017 00:00:00 GMT+0800 (中国标准时间)',
                start_time: '',
                // end_time: 'Sat Aug 19 2017 00:00:00 GMT+0800 (中国标准时间)',
                end_time: '',
                options: [],
                optionsValue: '',
                types: [{
                    name: '运行状态',
                    value: 'State'
                }, {
                    name: '输入线电压( V )',
                    value: 'PhaseVoltageInput'
                }, {
                    name: '输入线电压( V )',
                    value: 'LineVin'
                }, {
                    name: '输入线电流( A )',
                    value: 'LineIin'
                }, {
                    name: '输入相电压( V )',
                    value: 'PhaseVin'
                }, {
                    name: '输入相电流( A )',
                    value: 'PhaseIin'
                }, {
                    name: '输入功率( W )',
                    value: 'InputPower'
                }, {
                    name: '输出直流电压( V )',
                    value: 'DCVout'
                }, {
                    name: '输出直流电流( A )',
                    value: 'DCIout'
                }, {
                    name: '能效比',
                    value: 'EfficiencyRatio'
                }, {
                    name: '保护气体用量( M )',
                    value: 'GasFlow'
                }, {
                    name: '一次测温,二次测温',
                    value: 'Temperature'
                }, {
                    name: '过流报警',
                    value: 'OCAlarm'
                }, {
                    name: '过压报警',
                    value: 'OVAlarm'
                }],
                // typesValue: 'State'
                typesValue: ''
            },
            charts: '',
            chartsData: {
                date: []
            }
        }
    },
    watch: {
        '$route'(to, from) {
            // this.drawPie(this.$route.path.split('/')[2])
        }
    },
    methods: {
        drawPie(id) {
            this.charts.clear()
            // console.log(this.formInline['start_time'])
            // console.log(this.formInline['end_time'])
            // console.log(this.formInline['typesValue'])
            getHistoryData({
                factory_id: this.factoryId,
                factory_number: this.basicInfo['factory_number'],
                group_id: this.formInline['optionsValue'],
                start_time: dateFormat(this.formInline['start_time']),
                end_time: dateFormat(this.formInline['end_time']),
                search_field: this.formInline['typesValue'],
                equipment_id: this.equipmentId
            }).then(res => {
                if (res.code === 201) {
                    this.chartsData = res.data[0]
                    var chartsOptions = {
                        backgroundColor: '#394056',
                        tooltip: {
                            trigger: 'axis',
                            position: function(pt) {
                                return [pt[0], '10%']
                            }
                        },
                        title: {
                            left: 'center',
                            text: '',
                            textStyle: {
                                fontWeight: 'normal',
                                fontSize: 16,
                                color: '#F1F1F3'
                            }
                        },
                        toolbox: {
                            feature: {
                                dataZoom: {
                                    yAxisIndex: 'none'
                                },
                                restore: {},
                                saveAsImage: {}
                            }
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            axisLine: {
                                lineStyle: {
                                    color: '#57617B'
                                }
                            },
                            data: []
                        },
                        yAxis: {
                            type: 'value',
                            boundaryGap: [0, '100%'],
                            axisTick: {
                                show: false
                            },
                            axisLine: {
                                lineStyle: {
                                    color: '#57617B'
                                }
                            },
                            axisLabel: {
                                margin: 10,
                                textStyle: {
                                    fontSize: 14
                                }
                            },
                            splitLine: {
                                lineStyle: {
                                    color: '#57617B'
                                }
                            }
                        },
                        dataZoom: [{
                            type: 'inside',
                            start: 0,
                            end: 100
                        }, {
                            start: 0,
                            end: 10,
                            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                            handleSize: '80%',
                            handleStyle: {
                                color: '#57617B',
                                shadowBlur: 3,
                                shadowColor: 'rgba(0, 0, 0, 0.6)',
                                shadowOffsetX: 2,
                                shadowOffsetY: 2
                            },
                            textStyle: {
                                color: '#57617B'
                            },
                            borderColor: '#57617B'
                        }],
                        series: []
                    }
                    var colors = [{
                        beforeBg: 'rgba(137, 189, 27, 0.3)',
                        afterBg: 'rgba(137, 189, 27, 0)',
                        line: 'rgb(137,189,27)',
                        border: 'rgba(137,189,2,0.27)'
                    }, {
                        beforeBg: 'rgba(0, 136, 212, 0.3)',
                        afterBg: 'rgba(0, 136, 212, 0)',
                        line: 'rgb(0,136,212)',
                        border: 'rgba(0,136,212,0.2)'
                    }, {
                        beforeBg: 'rgba(219, 50, 51, 0.3)',
                        afterBg: 'rgba(219, 50, 51, 0)',
                        line: 'rgb(219,50,51)',
                        border: 'rgba(219,50,51,0.2)'
                    }]
                    var i = 0
                    chartsOptions.series = []
                    for (var key in this.chartsData) {
                        if (key === 'DateTime') {
                            chartsOptions.xAxis.data = this.chartsData[key]
                            // console.log(chartsOptions.xAxis.data)
                        } else if (key === '_id') {} else {
                            i = i + 1
                            // console.log(i)
                            chartsOptions.series.push({
                                name: key,
                                type: 'line',
                                smooth: true,
                                symbol: 'none',
                                sampling: 'average',
                                // itemStyle: {
                                //     normal: {
                                //         color: colors[i - 1]
                                //     }
                                // },
                                // areaStyle: {
                                //     normal: {
                                //         color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                //             offset: 0,
                                //             color: 'rgb(255, 158, 68)'
                                //         }, {
                                //             offset: 1,
                                //             color: 'rgb(255, 70, 131)'
                                //         }])
                                //     }
                                // },
                                lineStyle: {
                                    normal: {
                                        width: 1
                                    }
                                },
                                areaStyle: {
                                    normal: {
                                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: colors[i - 1]['beforeBg']
                                        }, {
                                            offset: 0.8,
                                            color: colors[i - 1]['afterBg']
                                        }], false),
                                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                                        shadowBlur: 10
                                    }
                                },
                                itemStyle: {
                                    normal: {
                                        color: colors[i - 1]['line'],
                                        borderColor: colors[i - 1]['border'],
                                        borderWidth: 12
                                    }
                                },
                                data: this.chartsData[key]
                            })
                        }
                    }
                    // console.log(chartsOptions.series)
                    this.charts.setOption(chartsOptions)
                }
            })
        },
        groupList() {
            getEquipmentBelongGroup({
                factory_id: this.factoryId,
                equipment_id: this.equipmentId
            }).then(res => {
                res.data.push({
                    name: '全部',
                    _id: ''
                })
                this.formInline.options = res.data
            })
        },
        queryFn() {
            getHistoryData({
                factory_id: this.factoryId,
                factory_number: this.basicInfo['factory_number'],
                group_id: this.formInline['optionsValue'],
                start_time: dateFormat(this.formInline['start_time']),
                end_time: dateFormat(this.formInline['end_time']),
                search_field: this.formInline['typesValue'],
                equipment_id: this.equipmentId
            }).then(res => {
                if (res.code === 201) {
                    this.chartsData = res.data
                }
            })
        },
        filterEcharts(_data) {
            switch (_data) {
            case _data.State:
                return '状态'
            default:
                return '没有数据'
            }
        }
    },
    // 调用
    mounted() {
        this.groupList()
        this.$nextTick(function() {
            this.charts = echarts.init(document.getElementById('main'))
            this.drawPie('main')
        })
        window.onresize = () => {
            this.charts.resize()
        }
    }
}
</script>
<style scoped>
#main {
    height: 600px;
    width: 100%;
}
</style>
