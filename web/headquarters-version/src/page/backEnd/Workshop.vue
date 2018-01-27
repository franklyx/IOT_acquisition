<template>
    <div>
        <el-form :inline="true" class="demo-form-inline" @submit.native.prevent v-if="isFormStatus">
            <el-form-item label="车间名称">
                <el-input v-model="workShopName" placeholder="车间名称" @keydown.enter.native="addWorkShopFn"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addWorkShopFn">添加</el-button>
            </el-form-item>
        </el-form>
        <div class="table-box">
            <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="name" align="center" min-width="150" label="车间名称"></el-table-column>
                <el-table-column prop="factory_name" align="center" min-width="150" label="公司"></el-table-column>
                <el-table-column align="center" min-width="150" label="操作" v-if="isFormStatus">
                    <template scope="scope">
                        <el-button type="text" size="small" @click="openDialog(scope.$index,scope.row)">编辑</el-button>
                        <el-button @click="deleteRow(scope.$index,scope.row)" type="text">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="dialog-box">
            <el-dialog title="编辑" :visible.sync="dialogFormVisible" size="tiny">
                <el-form @submit.native.prevent>
                    <el-form-item label="车间名称" :label-width="formLabelWidth">
                        <el-input v-model="editRow.name" auto-complete="off" @keydown.enter.native="modifyWorkShopFn"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="modifyWorkShopFn">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
import {
    mapGetters
} from 'vuex'
import { getWorkShop, addWorkShop, modifyWorkShop, deleteWorkShop } from '@/service/api'
export default {
    mounted() {
        this.initWorkShop()
    },
    computed: {
        ...mapGetters(['getFactoryId', 'isFormStatus'])
    },
    methods: {
        initWorkShop() {
            const loading = this.$loading({
                target: '.table-box',
                text: '拼命加载中'
            })
            getWorkShop({
                id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.code === 201) {
                    this.tableData = res.data
                }
            }).then(res => {
                loading.close()
            })
        },
        addWorkShopFn() {
            addWorkShop({
                id: this.getFactoryId,
                name: this.workShopName
            }).then(res => {
                if (res.code === 201) {
                    this.$message({
                        type: 'success',
                        message: '车间添加成功!',
                        duration: 2 * 1000
                    })
                    this.initWorkShop()
                }
            })
        },
        deleteRow(index, rows) {
            deleteWorkShop({
                factory_id: this.getFactoryId,
                workshop_id: rows['_id']
            }).then(res => {
                if (res.code === 204) {
                    this.$message({
                        type: 'success',
                        message: '车间删除成功!',
                        duration: 2 * 1000
                    })
                    this.initWorkShop()
                } else if (res.code === 411) {
                    this.$message({
                        type: 'warning',
                        message: '车间禁止删除!',
                        duration: 2 * 1000
                    })
                }
            })
        },
        modifyWorkShopFn() {
            modifyWorkShop({
                factory_id: this.getFactoryId,
                workshop_id: this.editRow['_id'],
                name: this.editRow.name
            }).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '车间修改成功!',
                        duration: 2 * 1000
                    })
                    this.initWorkShop()
                    this.dialogFormVisible = false
                }
            })
        },
        // changeFactory(){
        //  getWorkShop({id:this.getFactoryId},{page:1,per_page:10}).then(res=>{
        //    this.tableData = res.data
        //  })
        // },
        openDialog(index, rows) {
            this.editRow = rows
            this.dialogFormVisible = true
        }
    },
    data() {
        return {
            factoryList: [],
            selectFactory: '',
            workShopName: '',
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
