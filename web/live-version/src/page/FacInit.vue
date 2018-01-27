<template>
    <div class="box">
        <el-row type="flex" justify="center" class="row-bg">
            <el-col :xs="20" :sm="12" :md="12" :lg="10">
                <el-card class="box-card" v-if="initUserStatus">
                    <div slot="header" class="clearfix">
                        <h1>请注册用户</h1>
                    </div>
                    <div class="text item">
                        <el-form ref="form" label-width="80px">
                            <el-form-item label="用户名">
                                <el-input v-model="username"></el-input>
                            </el-form-item>
                            <el-form-item label="密码">
                                <el-input v-model="password" type="password"></el-input>
                            </el-form-item>
                            <el-form-item label-width="80px">
                                <el-button type="primary" @click="initAdminFn">立即注册</el-button>
                            </el-form-item>
                        </el-form>
                    </div>
                </el-card>
                <el-card class="box-card" v-if="initFacStatus">
                    <div slot="header" class="clearfix">
                        <h1>请初始化工厂</h1>
                    </div>
                    <div class="text item">
                        <el-form ref="form" label-width="80px">
                            <el-form-item label="工厂名称">
                                <el-input v-model="factory_name"></el-input>
                            </el-form-item>
                            <el-form-item label-width="80px">
                                <el-button type="primary" @click="initFacFn">立即初始化</el-button>
                            </el-form-item>
                        </el-form>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>
<script>
import {
    initAdmin,
    addFactory
} from '@/service/api'
import storage from '@/util/storage'
export default {
    data() {
        return {
            factory_name: '',
            username: '',
            password: '',
            initFacStatus: false,
            initUserStatus: true
        }
    },
    methods: {
        initAdminFn() {
            initAdmin({
                username: this.username,
                password: this.password
            }).then(res => {
                if (res.code === 201) {
                    this.initFacStatus = true
                    this.initUserStatus = false
                    const user = {
                        token: res.data.token,
                        rf_token: res.data.rf_token
                    }
                    storage.set('user', user)
                }
            })
        },
        initFacFn() {
            addFactory({
                name: this.factory_name
            }).then(res => {
                if (res.code === 201) {
                    this.$router.push({
                        path: '/login'
                    })
                }
            })
        }
    }
}
</script>
<style scoped>
.text {
    font-size: 14px;
}

.item {
    padding: 18px 0;
}

.row-bg {
    align-items: center;
    height: 90vh;
}
</style>
