<template>
    <div>
        <el-form :inline="true" :model="formInline" class="demo-form-inline" @submit.native.prevent v-if="isFormStatus">
            <el-form-item label="车间名称">
                <el-select v-model="formInline.selectWorkShop" placeholder="车间名称" @change="changeWorkShop">
                    <el-option v-for="item in workShopList" :key="item._id" :label="item.name" :value="item._id">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="生产线名称">
                <el-select v-model="formInline.selectProLine" placeholder="生产线名称">
                    <el-option v-for="item in proLineList" :key="item._id" :label="item.name" :value="item._id">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="设备名称">
                <el-input v-model="formInline.deviceName" placeholder="出厂编号"></el-input>
            </el-form-item>
            <el-form-item label="出厂编号">
                <el-input v-model="formInline.factory_number" placeholder="出厂编号"></el-input>
            </el-form-item>
            <el-form-item label="出厂时间">
                <el-date-picker v-model="formInline.factory_time" type="date" placeholder="选择出厂时间"> </el-date-picker>
            </el-form-item>
            <el-form-item label="产品型号">
                <!-- <el-input v-model="formInline.product_number" placeholder="产品型号" @keydown.enter.native="addDeviceFn"></el-input> -->
                <el-select v-model="formInline.product_number" placeholder="产品型号">
                    <el-option v-for="item in productNumberList" :key="item.number" :label="item.number" :value="item.number">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addDeviceFn">添加</el-button>
            </el-form-item>
        </el-form>
        <div class="table-box">
            <el-table :data="tableData" style="width: 100%">
                <el-table-column  :key="tableData.name" align="center" min-width="150" prop="name" label="设备名称"></el-table-column>
                <el-table-column  :key="tableData.factory_name" align="center" min-width="150" prop="factory_name" label="公司名称" ></el-table-column>
                <el-table-column  :key="tableData.workshop_name" align="center" min-width="150" prop="workshop_name" label="车间名称" ></el-table-column>
                <el-table-column  :key="tableData.line_name" align="center" min-width="150" prop="line_name" label="生产线名称" ></el-table-column>
                <el-table-column  :key="tableData.factory_number" align="center" min-width="150" prop="factory_number" label="出厂编号" ></el-table-column>
                <el-table-column  :key="tableData.factory_time" align="center" min-width="150" prop="factory_time" label="出场时间" ></el-table-column>
                <el-table-column  :key="tableData.product_number" align="center" min-width="150" prop="product_number" label="产品型号" ></el-table-column>
                <el-table-column label="操作" align="center" min-width="150" v-if="isFormStatus">
                    <template scope="scope">
                        <el-button type="text" size="small" @click="openDialog(scope.$index,scope.row)">编辑</el-button>
                        <el-button @click="deleteRow(scope.$index,scope.row)" type="text">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="dialog-box">
            <el-dialog title="编辑" :visible.sync="dialogFormVisible" size="tiny">
                <el-form :model="editRow">
                    <el-row>
                      <el-col :xs="24" :sm="24" :md="24" :lg="24">
                        <el-form-item label="设备名称" :label-width="formLabelWidth">
                            <el-input v-model="editRow.name" auto-complete="off"></el-input>
                        </el-form-item>
                      </el-col>
                    </el-row>
                    <el-form-item label="车间名称" :label-width="formLabelWidth">
                       <el-select v-model="editRow.workshop_id" placeholder="车间名称" @change="changeDialogWorkShop">
                          <el-option v-for="item in workShopList" :key="item._id" :label="item.name" :value="item._id">
                          </el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="生产线名称" :label-width="formLabelWidth">
                       <el-select v-model="editRow.line_id" placeholder="生产线名称">
                           <el-option v-for="item in proLineList" :key="item._id" :label="item.name" :value="item._id">
                           </el-option>
                       </el-select>
                    </el-form-item>
                    <el-form-item label="出厂编号" :label-width="formLabelWidth">
                        <el-input v-model="editRow.factory_number" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="出厂时间" :label-width="formLabelWidth">
                        <el-date-picker v-model="editRow.factory_time" type="date" placeholder="选择出厂时间"> </el-date-picker>
                    </el-form-item>
                    <el-form-item label="产品型号" :label-width="formLabelWidth">
                        <!-- <el-input v-model="editRow.product_number" auto-complete="off"></el-input> -->
                        <el-select v-model="editRow.product_number" placeholder="产品型号">
                            <el-option v-for="item in productNumberList" :key="item.number" :label="item.number" :value="item.number">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="modifyDeviceFn">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
import {
    getDevice,
    addDevice,
    getWorkShop,
    getProductList,
    getLineUnderShop,
    modifyDevice,
    deleteDevice
} from '@/service/api'
import {
    mapGetters
} from 'vuex'
import {
    dateFormat
} from '@/util/dateFormat'
export default {
    computed: {
        ...mapGetters(['getFactoryId', 'isFormStatus'])
    },
    mounted() {
        this.initDevice()
        this.getWorkShopFn()
        this.getProductListFn()
    },
    methods: {
        changeWorkShop() {
            getLineUnderShop({
                factory_id: this.getFactoryId,
                workshop_id: this.formInline.selectWorkShop
            }).then(res => {
                this.proLineList = res.data
            })
        },
        changeDialogWorkShop() {
            getLineUnderShop({
                factory_id: this.getFactoryId,
                workshop_id: this.editRow.workshop_id
            }).then(res => {
                this.proLineList = res.data
            })
        },
        initDevice() {
            const loading = this.$loading({
                target: '.table-box',
                text: '拼命加载中'
            })
            getDevice({
                factory_id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.code === 201) {
                    this.tableData = res.data
                }
                loading.close()
            })
        },
        getWorkShopFn() {
            getWorkShop({
                id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                this.workShopList = res.data
            })
        },
        getProductListFn() {
            getProductList({
                factory_id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.code === 201) {
                    this.productNumberList = res.data
                }
            })
        },
        addDeviceFn() {
            addDevice({
                factory_id: this.getFactoryId,
                name: this.formInline.deviceName,
                workshop_id: this.formInline.selectWorkShop,
                line_id: this.formInline.selectProLine,
                factory_number: this.formInline.factory_number,
                factory_time: dateFormat(this.formInline.factory_time),
                product_number: this.formInline.product_number
            }).then(res => {
                if (res.code === 201) {
                    this.$message({
                        type: 'success',
                        message: '添加成功!',
                        duration: 2 * 1000
                    })
                    this.initDevice()
                }
            })
        },
        modifyDeviceFn() {
            modifyDevice({
                factory_id: this.getFactoryId,
                equipment_id: this.editRow['_id'],
                name: this.editRow.name,
                workshop_id: this.editRow.workshop_id,
                line_id: this.editRow.line_id,
                factory_number: this.editRow.factory_number,
                factory_time: dateFormat(this.editRow.factory_time),
                product_number: this.editRow.product_number
            }).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2 * 1000
                    })
                    this.dialogFormVisible = false
                    this.initDevice()
                }
            })
        },
        deleteRow(index, rows) {
            deleteDevice({
                factory_id: rows.factory_id,
                equipment_id: rows._id
            }).then(res => {
                if (res.code === 204) {
                    this.$message({
                        type: 'success',
                        message: '删除成功!',
                        duration: 2 * 1000
                    })
                    this.initDevice()
                }
            })
        },
        openDialog(index, rows) {
            this.editRow = rows
            this.changeDialogWorkShop()
            this.dialogFormVisible = true
        }
    },
    data() {
        return {
            workShopList: [],
            productNumberList: [],
            proLineList: [],
            formInline: {
                selectWorkShop: '',
                selectProLine: '',
                deviceName: '',
                factory_number: '',
                factory_time: '',
                product_number: ''
            },
            tableData: [],
            dialogFormVisible: false,
            formLabelWidth: '100px',
            editRow: {}
        }
    }
}
</script>
<style>

</style>
