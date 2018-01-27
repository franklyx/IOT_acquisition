<template>
    <div>
        <el-form :inline="true" class="demo-form-inline" :model="roleForm" ref="roleForm" @submit.native.prevent v-if="isFormStatus">
            <el-form-item label="车间名称" prop="selectWorkShop">
                <el-select v-model="roleForm.selectWorkShop" placeholder="请选择车间名称" @change="changeWorkShop">
                    <el-option v-for="item in workShopList" :key="item._id" :label="item.name" :value="item._id">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="生产线名称" prop="lineName">
                <el-input v-model="roleForm.lineName" placeholder="生产线名称" @keydown.enter.native="addLine"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addLine">添加</el-button>
            </el-form-item>
        </el-form>
        <div class="table-box">   
            <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="name"  align="center" min-width="150" label="生产线"></el-table-column>
                <el-table-column prop="factory_name"  align="center" min-width="150" label="公司"></el-table-column>
                <el-table-column prop="workshop_name"  align="center" min-width="150" label="车间"></el-table-column>
                <el-table-column  align="center" min-width="150" label="操作" v-if="isFormStatus">
                    <template scope="scope">
                        <el-button type="text" size="small" @click="openDialog(scope.$index,scope.row)">编辑</el-button>
                        <el-button @click="deleteRow(scope.$index,scope.row)" type="text">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="dialog-box">
            <el-dialog title="编辑" :visible.sync="dialogFormVisible" size="tiny">
                <el-form>
                    <el-form-item label="车间名称" :label-width="formLabelWidth">
                        <el-select v-model="editRow.workshop_id" placeholder="请选择" @change="changeWorkShop">
                            <el-option v-for="item in workShopList" :key="item._id" :label="item.name" :value="item._id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="生产线名称" :label-width="formLabelWidth">
                        <el-input v-model="editRow.name" auto-complete="off"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="modifyProLineFn">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
import {
    getWorkShop,
    getProductLine,
    addProductLine,
    modifyProLine,
    deleteProLine
} from '@/service/api'
import {
    mapGetters
} from 'vuex'
export default {
    mounted() {
        getWorkShop({
            id: this.getFactoryId,
            page: 1,
            per_page: 99999
        }).then(res => {
            if (res.code === 201) {
                this.workShopList = res.data
            }
        }).catch(err => {
            console.log(err)
        })
        this.getProductLineFn()
    },
    computed: {
        ...mapGetters(['getFactoryId', 'isFormStatus'])
    },
    methods: {
        addLine() {
            addProductLine({
                factory_id: this.getFactoryId,
                name: this.roleForm.lineName,
                workshop_id: this.roleForm.selectWorkShop
            }).then(res => {
                if (res.code === 201) {
                    this.$message({
                        type: 'success',
                        message: '添加成功!',
                        duration: 2 * 1000
                    })
                    this.getProductLineFn()
                    this.$refs['roleForm'].resetFields()
                }
            })
        },
        deleteRow(index, rows) {
            deleteProLine({
                factory_id: rows['factory_id'],
                productline_id: rows['_id']
            }).then(res => {
                if (res.code === 204) {
                    this.$message({
                        type: 'success',
                        message: '删除成功!',
                        duration: 2 * 1000
                    })
                    this.getProductLineFn()
                }
            })
        },
        openDialog(index, rows) {
            this.editRow = rows
            this.dialogFormVisible = true
        },
        changeFactory() {
            getWorkShop({
                id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                this.workShopList = res.data
            })
            this.getProductLineFn()
        },
        getProductLineFn() {
            const loading = this.$loading({
                target: '.table-box',
                text: '拼命加载中'
            })
            getProductLine({
                id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.code === 201) {
                    this.tableData = res.data
                }
            }).then(res => {
                loading.close()
            }).catch(err => {
                console.log(err)
            })
        },
        changeWorkShop() {

        },
        modifyProLineFn() {
            modifyProLine({
                factory_id: this.editRow['factory_id'],
                productline_id: this.editRow['_id'],
                name: this.editRow['name'],
                workshop_id: this.editRow['workshop_id']
            }).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2 * 1000
                    })
                    this.getProductLineFn()
                    this.dialogFormVisible = false
                }
            })
        }
    },
    data() {
        return {
            factoryList: [],
            workShopList: [],
            selectFactory: '',
            roleForm: {
                selectWorkShop: '',
                lineName: ''
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
