<template>
    <transition enter-active-class="animated bounceInUp">
        <div>
            <div class="selectTab">
                <el-form :inline="true" :model="form" class="demo-form-inline">
                    <el-form-item label="时间">
                        <el-date-picker v-model="form.date" type="month" placeholder="选择日期"> </el-date-picker>
                    </el-form-item>
                    <el-form-item label="类型">
                        <el-select v-model="form.search_field" placeholder="请选择">
                            <el-option v-for="item in options" :key="item.value" :label="item.name" :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="initData">查询</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <el-table style="width: 100%" :data="tableData" v-if="tableData[0]">
                <el-table-column label="日期" align="center" data="date" v-if="tableData[0].date">
                    <template scope="scope">
                        <span>{{ scope.row.date }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="运行状态" align="center" v-if="tableData[0].State">
                    <template scope="scope">
                        <span>{{ scope.row.State }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="输入电压相位" align="center" v-if="tableData[0].PhaseVoltageInput">
                    <template scope="scope">
                        <span>{{ scope.row.PhaseVoltageInput }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="输入线电压(V)" align="center" v-if="tableData[0].LineVin">
                    <template scope="scope">
                        <span>{{ scope.row.LineVin }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="输入线电流(A)" align="center" v-if="tableData[0].LineIin">
                    <template scope="scope">
                        <span>{{ scope.row.LineIin }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="PhaseVinAB" align="center" v-if="tableData[0].PhaseVinAB">
                    <template scope="scope">
                        <span>{{ scope.row.PhaseVinAB }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="PhaseVinBC" align="center" v-if="tableData[0].PhaseVinBC">
                    <template scope="scope">
                        <span>{{ scope.row.PhaseVinBC }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="PhaseIinAB" align="center" v-if="tableData[0].PhaseIinAB">
                    <template scope="scope">
                        <span>{{ scope.row.PhaseIinAB }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="PhaseIinBC" align="center" v-if="tableData[0].PhaseIinBC">
                    <template scope="scope">
                        <span>{{ scope.row.PhaseIinBC }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="PhaseIinCA" align="center" v-if="tableData[0].PhaseIinCA">
                    <template scope="scope">
                        <span>{{ scope.row.PhaseIinCA }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="输入功率(W)" align="center" v-if="tableData[0].InputPower">
                    <template scope="scope">
                        <span>{{ scope.row.InputPower }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="输出直流电压(V)" align="center" v-if="tableData[0].DCVout">
                    <template scope="scope">
                        <span>{{ scope.row.DCVout }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="输出直流电流(A)" align="center" v-if="tableData[0].DCIout">
                    <template scope="scope">
                        <span>{{ scope.row.DCIout }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="能效比" align="center" v-if="tableData[0].EfficiencyRatio">
                    <template scope="scope">
                        <span>{{ scope.row.EfficiencyRatio }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="保护气体用量(m3)" align="center" v-if="tableData[0].GasFlow">
                    <template scope="scope">
                        <span>{{ scope.row.GasFlow }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="Temperature1" align="center" v-if="tableData[0].Temperature1">
                    <template scope="scope">
                        <span>{{ scope.row.Temperature1 }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="Temperature2" align="center" v-if="tableData[0].Temperature2">
                    <template scope="scope">
                        <span>{{ scope.row.Temperature2 }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="过流报警" align="center" v-if="tableData[0].OCAlarm || tableData[0].OCAlarm === 0">
                    <template scope="scope">
                        <span>{{ scope.row.OCAlarm }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="过压报警" align="center" v-if="tableData[0].OVAlarm || tableData[0].OVAlarm === 0">
                    <template scope="scope">
                        <span>{{ scope.row.OVAlarm }}</span>
                    </template>
                </el-table-column> -->
                <!-- <el-table-column  prop="State" label="状态"align="center"></el-table-column> -->
            </el-table>
        </div>
    </transition>
</template>
<script>
import {
    getReportData
} from '@/service/api'
import {
    mouthFormat
} from '@/util/dateFormat'
export default {
    props: ['equipmentId', 'factoryId', 'basicInfo'],
    data() {
        return {
            tableData: [],
            options: [{
                name: '运行状态',
                value: 'State'
            }, {
                name: '输入电压相位',
                value: 'PhaseVoltageInput'
            }, {
                name: '输入线电压(V)',
                value: 'LineVin'
            }, {
                name: '输入线电流(A)',
                value: 'LineIin'
            }, {
                name: '输入相电压(V)',
                value: 'PhaseVin'
            }, {
                name: '输入相电流(A)',
                value: 'PhaseIin'
            }, {
                name: '输入功率(W)',
                value: 'InputPower'
            }, {
                name: '输出直流电压(V)',
                value: 'DCVout'
            }, {
                name: '输出直流电流(A)',
                value: 'DCIout'
            }, {
                name: '能效比',
                value: 'EfficiencyRatio'
            }, {
                name: '保护气体用量(m3)',
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
            form: {
                search_field: '',
                date: ''
            }
        }
    },
    mounted() {},
    methods: {
        // getReportData({}).then(res=>{

        // })
        initData() {
            getReportData({
                factory_id: this.factoryId,
                date: mouthFormat(this.form['date']),
                search_field: this.form['search_field'],
                equipment_id: this.equipmentId
            }).then(res => {
                if (res.code === 201) {
                    this.$nextTick(function() {
                        this.tableData = res.data
                    })
                }
            })
        }
    }
}
</script>
<style scoped>
.selectTab {
    margin-bottom: 20px;
}
</style>
