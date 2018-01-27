<template>
    <div>
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
            <el-form-item label="用户名">
                <el-input v-model="formInline.username" placeholder="用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码">
                <el-input v-model="formInline.password"  placeholder="密码"></el-input>
            </el-form-item>
            <el-form-item label="权限">
                <!-- <el-input v-model="formInline.role" placeholder="权限"></el-input> -->
                <el-select v-model="formInline.role" placeholder="请选择角色">
                    <el-option v-for="item in roles" :key="item.value" :label="item.text" :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addUser">添加</el-button>
            </el-form-item>
        </el-form>
        <el-table :data="tableData" style="width: 100%" stripe>
            <el-table-column prop="username" align="center" min-width="180" label="用户名"></el-table-column>
            <el-table-column prop="password" align="center" min-width="180" label="密码">
                 <template scope="scope">
                    <input type="password" value="scope.row.password" readonly="readonly" class="table-input" />
                </template>
            </el-table-column>
            <el-table-column prop="user_role" align="center" min-width="180" label="权限">
                <template scope="scope">
                    <span>{{scope.row.user_role | filterA}}</span>
                </template>
            </el-table-column>
            <el-table-column align="center" min-width="180" label="操作">
                <template scope="scope">
                    <el-button type="text" size="small" @click="openDialog(scope.$index,scope.row)">编辑</el-button>
                    <el-button @click="deleteRow(scope.$index,scope.row)" type="text">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <div class="dialog-box">
            <el-dialog title="编辑" :visible.sync="dialogFormVisible" size="tiny">
                <el-form>
                    <el-form-item label="用户名" :label-width="formLabelWidth">
                        <el-input v-model="editRow.username" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" :label-width="formLabelWidth" >
                        <el-input v-model="editRow.password" auto-complete="off" type="password"></el-input>
                    </el-form-item>
                    <el-form-item label="权限" :label-width="formLabelWidth">
                        <el-select v-model="editRow.user_role" placeholder="请选择">
                            <el-option v-for="item in roles" :key="item.value" :label="item.text" :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="modifyRow">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
import {
    getUserList,
    addUser,
    deleteUser,
    modifyUser
} from '@/service/api'
import {
    mapGetters
} from 'vuex'
export default {
    filters: {
        filterA: function(value) {
            switch (value) {
            case 0:
                return '用户'
            case 1:
                return '管理员'
            case 2:
                return '超级管理员'
            }
        }
    },
    methods: {
        addUser() {
            addUser({
                name: this.formInline['username'],
                password: this.formInline['password'],
                factory_id: this.getFactoryId,
                role: this.formInline['role']
            }).then(res => {
                if (res.code === 201) {
                    this.$message({
                        type: 'success',
                        message: '添加成功!',
                        duration: 2 * 1000
                    })
                    this.getUserListFn()
                } else if (res.msg === 'Username already exists') {
                    this.$message({
                        type: 'error',
                        message: '用户名已存在!',
                        duration: 2 * 1000
                    })
                }
            })
        },
        deleteRow(index, rows) {
            deleteUser({
                id: rows._id
            }).then(res => {
                console.log(res)
                if (res.code === 204) {
                    this.$message({
                        type: 'success',
                        message: '删除成功!',
                        duration: 2 * 1000
                    })
                    this.getUserListFn()
                }
            })
        },
        modifyRow() {
            modifyUser({
                id: this.editRow['_id'],
                name: this.editRow.username,
                password: this.editRow.password,
                role: this.editRow.user_role,
                factory_id: this.getFactoryId
            }).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2 * 1000
                    })
                    this.getUserListFn()
                    this.dialogFormVisible = false
                }
            })
        },
        openDialog(index, rows) {
            this.editRow = rows
            this.dialogFormVisible = true
        },
        getUserListFn() {
            const loding = this.$loading({
                target: 'table'
            })
            getUserList({
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.data !== '') {
                    this.tableData = res.data
                }
                loding.close()
            }).catch(err => {
                console.log(err)
            })
        }
    },
    mounted() {
        this.getUserListFn()
    },
    computed: {
        ...mapGetters(['getFactoryId'])
    },
    data() {
        return {
            roles: [{
                value: 1,
                text: '管理员'
            }, {
                value: 0,
                text: '用户'
            }],
            formInline: {
                username: '',
                password: '',
                role: ''
            },
            tableData: [],
            dialogFormVisible: false,
            formLabelWidth: '100px',
            editRow: {}
        }
    }
}
</script>
<style scoped>
.table-input{
    border: none;
    background: transparent;
    text-align: center;
}
</style>
