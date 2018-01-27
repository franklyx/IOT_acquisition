<style scoped lang="scss">
.header {
    background: #324157;
    height: 50px;
    .title {
        font-size: 20px;
        padding-left: 20px;
        line-height: 50px;
        color: #fff;
        display: inline-block;
    }
    .dropdown {
        line-height: 50px;
        margin-right: 20px;
        font-size: 14px;
        display: inline-block;
        color: #fff;
        .el-dropdown {
            color: #fff;
        }
    }
    .logout {
        padding-right: 20px;
    }
}

@media (max-width: 768px) {
    .header {
        .title {
            display: none;
        }
    }
}
</style>
<template>
    <div class="header">
        <h2 class="title">焊机设备信息化管理平台</h2>
        <!-- <router-link to="/index" class="title" tag="h2">焊机设备信息化管理平台</router-link> -->
        <div class="fr">
            <div class="dropdown">
                <el-dropdown trigger="click">
                    <span class="el-dropdown-link">
                   {{getUserName}}<i class="el-icon-caret-bottom el-icon--right"></i>
                </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item v-if="getRole === 1">
                            <router-link to="/index" tag="p">前台展示</router-link>
                        </el-dropdown-item>
                        <el-dropdown-item v-if="getRole === 0">
                            <p @click="openDialog">修改密码</p>
                        </el-dropdown-item>
                        <el-dropdown-item>
                            <router-link to="/supervise/user" tag="p" v-if="getRole === 1">后台管理</router-link>
                        </el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </div>
            <a href="javascript:void(0)" class="logout">
                <el-button type="primary" @click="loginOutFn">退出</el-button>
            </a>
        </div>
        <div class="dialog-box">
            <el-dialog title="账号设置" :visible.sync="dialogFormVisible" size="tiny" :modalAppendToBody="false">
                <el-form :model="editRow" @keydown.enter.native="modifyUser">
                    <el-row>
                      <el-col :xs="24" :sm="24" :md="24" :lg="24">
                        <el-form-item label="账号" label-width="100px">
                            <el-input v-model="editRow.username" auto-complete="off"></el-input>
                        </el-form-item>
                      </el-col>
                    </el-row>
                    <el-form-item label="新密码" label-width="100px">
                        <el-input v-model="editRow.password" auto-complete="off"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="modifyUser">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
import {
    mapGetters
} from 'vuex'
import { modifyUserinform } from '@/service/api'
export default {
    data() {
        return {
            spanLeft: 5,
            spanRight: 19,
            dialogFormVisible: false,
            editRow: {}
        }
    },
    computed: {
        ...mapGetters(['getUserName', 'getRole', 'getUserId'])
    },
    methods: {
        loginOutFn() {
            this.$confirm('您将退出当前账号, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                // this.$message({
                //     type: 'success',
                //     message: '退出成功!',
                //     duration: 2 * 1000
                // })
                this.$store.dispatch('loginOut').then(res => {
                    this.$router.push({
                        path: '/login'
                    })
                })
            }).catch(() => {})
        },
        modifyUser() {
            modifyUserinform({user_id: this.getUserId, name: this.getUserName, password: this.editRow.password}).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2 * 1000
                    })
                    this.$router.push('/login')
                }
            })
        },
        openDialog(index, rows) {
            this.editRow.username = this.getUserName
            this.dialogFormVisible = true
        }
    }
}
</script>
