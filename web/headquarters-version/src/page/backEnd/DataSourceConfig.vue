<template>
    <div>
        <el-button type="text" @click="addDialog('formData')">添加数据源</el-button>
        <div class="dialog-box">
            <el-dialog title="编辑" :visible.sync="dialogFormVisible" size="tiny">
               <el-form :model="formData" ref="formData" label-width="100px"> 
                   <el-form-item prop="name" label="数据源名称">
                       <el-input v-model="formData.name"></el-input>
                   </el-form-item>
                   <el-form-item prop="user" label=" mqtt用户名">
                       <el-input v-model="formData.user"></el-input>
                   </el-form-item>
                   <el-form-item prop="passwd" label=" mqtt密码">
                       <el-input v-model="formData.passwd"></el-input>
                   </el-form-item>
                   <el-form-item prop="host" label=" mqtt主机">
                       <el-input v-model="formData.host"></el-input>
                   </el-form-item>
                   <el-form-item prop="port" label="mqtt端口">
                       <el-input v-model="formData.port"></el-input>
                   </el-form-item>
                   <el-form-item prop="topic" label="推送主题">
                       <el-input v-model="formData.topic"></el-input>
                   </el-form-item>
                   <el-form-item prop="qos" label="推送质量">
                       <el-radio-group v-model="formData.qos">
                           <el-radio-button label="1">低质量</el-radio-button>
                           <el-radio-button label="2">高质量</el-radio-button>
                       </el-radio-group>
                   </el-form-item>
                   <el-form-item prop="retain" label="保留消息">
                       <el-radio-group v-model="formData.retain">
                           <el-radio-button label="true">是</el-radio-button>
                           <el-radio-button label="false">否</el-radio-button>
                       </el-radio-group>
                   </el-form-item>
                   <el-form-item prop="keepalive" label="心跳间隔">
                       <el-slider v-model="formData.keepalive" :step="10" show-stops>
                       </el-slider>
                   </el-form-item>
                   <el-form-item prop="status" label="运行状态">
                       <el-radio-group v-model="formData.status">
                           <el-radio-button label="active">active</el-radio-button>
                           <el-radio-button label="stopped">stopped</el-radio-button>
                       </el-radio-group>
                   </el-form-item>
               </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="addSourceFn" v-show="isAdd">提交</el-button>
                    <el-button type="primary" @click="modifySourceFn" v-show="isModify">修改</el-button>
                </div>
            </el-dialog>
        </div>
        <el-table :data="tableData" style="width: 100%" stripe>
            <el-table-column type="expand">
                <template scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                        <el-form-item label="数据源名称">
                            <span>{{ props.row.name }}</span>
                        </el-form-item>
                        <el-form-item label="mqtt用户名">
                            <span>{{ props.row.user }}</span>
                        </el-form-item>
                        <el-form-item label="mqtt密码">
                            <span>{{ props.row.passwd }}</span>
                        </el-form-item>
                        <el-form-item label="mqtt主机">
                            <span>{{ props.row.host }}</span>
                        </el-form-item>
                        <el-form-item label="mqtt端口">
                            <span>{{ props.row.port }}</span>
                        </el-form-item>
                        <el-form-item label="推送主题">
                            <span>{{ props.row.topic }}</span>
                        </el-form-item>
                        <el-form-item label="推送质量">
                            <span>{{ props.row.qos }}</span>
                        </el-form-item>
                        <el-form-item label="心跳间隔">
                            <span>{{ props.row.keepalive }}</span>
                        </el-form-item>
                        <el-form-item label="运行状态">
                            <span>{{ props.row.status }}</span>
                        </el-form-item>
                    </el-form>
                </template>
            </el-table-column>
            <el-table-column prop="name" align="center" min-width="180" label="数据源名称"></el-table-column>
            <el-table-column prop="user" align="center" min-width="180" label="mqtt用户名"></el-table-column>
            <el-table-column prop="passwd" align="center" min-width="180" label="mqtt密码"></el-table-column>
            <el-table-column prop="host" align="center" min-width="180" label="mqtt主机"></el-table-column>
            <el-table-column prop="port" align="center" min-width="180" label="mqtt端口"></el-table-column>
           <!--  <el-table-column prop="topic" align="center" min-width="180" label="推送主题"></el-table-column>
            <el-table-column prop="qos" align="center" min-width="180" label="推送质量"></el-table-column>
            <el-table-column prop="keepalive" align="center" min-width="180" label="心跳间隔"></el-table-column>-->
            <el-table-column prop="status" align="center" min-width="180" label="运行状态">
                <template scope="scope">
                    <el-switch v-model="scope.row.status" on-text="on" off-text="off"  on-value="active"
    off-value="stopped" @change="modifyStatus(scope.$index,scope.row)"></el-switch>
                </template>
            </el-table-column> 
            <!-- <el-table-column prop="retain" align="center" min-width="180" label="保留消息"></el-table-column> -->
            <el-table-column align="center" min-width="180" label="操作">
                <template scope="scope">
                    <el-button type="text" size="small" @click="openDialog(scope.$index,scope.row)">编辑</el-button>
                    <el-button @click="deleteRow(scope.$index,scope.row)" type="text">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>
<script>
import {
    mapGetters
} from 'vuex'
import {
    getSourceList,
    addSource,
    deleteSource,
    modifySource
} from '@/service/api'

export default {
    mounted() {
        this.initData()
    },
    computed: {
        ...mapGetters(['isFormStatus'])
    },
    methods: {
        addSourceFn() {
            addSource({
                name: this.formData['name'],
                user: this.formData['user'],
                passwd: this.formData['passwd'],
                host: this.formData['host'],
                port: this.formData['port'],
                topic: this.formData['topic'],
                qos: this.formData['qos'],
                retain: this.formData['retain'],
                keepalive: this.formData['keepalive'],
                status: this.formData['status']
            }).then(res => {
                if (res.code === 201) {
                    this.$message({
                        type: 'success',
                        message: '添加成功!',
                        duration: 2 * 1000
                    })
                    this.dialogFormVisible = false
                    this.initData()
                }
            })
        },
        initData() {
            getSourceList({
                page: 1,
                per_page: 999999
            }).then(res => {
                this.tableData = res.data
            })
        },
        addDialog(formName) {
            this.dialogFormVisible = true
            if (this.$refs.formData) {
                this.$refs.formData.resetFields()
            }
        },
        modifySourceFn() {
            modifySource({
                source_id: this.formData['_id'],
                name: this.formData['name'],
                user: this.formData['user'],
                passwd: this.formData['passwd'],
                host: this.formData['host'],
                port: this.formData['port'],
                topic: this.formData['topic'],
                qos: this.formData['qos'],
                retain: this.formData['retain'],
                keepalive: this.formData['keepalive'],
                status: this.formData['status']
            }).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2 * 1000
                    })
                    this.dialogFormVisible = false
                    this.initData()
                }
            })
        },
        modifyStatus(index, rows) {
            let newStatus = rows['status'] === 'active' ? newStatus = 'stopped' : newStatus = 'active'
            modifySource({
                source_id: rows['_id'],
                status: newStatus
            }).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2 * 1000
                    })
                    this.initData()
                }
            })
        },
        openDialog(index, rows) {
            console.log('edit open dialog.......')
            this.dialogFormVisible = true
            this.formData = rows
            this.isAdd = false
            this.isModify = true
        },
        deleteRow(index, rows) {
            deleteSource({
                source_id: rows['_id']
            }).then(res => {
                if (res.code === 204) {
                    this.$message({
                        type: 'success',
                        message: '删除成功!',
                        duration: 2 * 1000
                    })
                    this.initData()
                }
            })
        }
    },
    data() {
        return {
            isForm: false,
            tableData: [],
            dialogVisible: false,
            dialogFormVisible: false,
            formData: {
                name: '',
                user: '',
                passwd: '',
                host: '',
                port: 1883,
                qos: 2,
                retain: true,
                keepalive: 60,
                status: 'active',
                topic: ''
            },
            labelWidth: '100px',
            isAdd: true,
            isModify: false
        }
    }
}
</script>
<style scoped>
.time {
    font-size: 13px;
    color: #999;
}

.bottom {
    margin-top: 13px;
    line-height: 12px;
}

.button {
    padding: 0;
    float: right;
}

.image {
    width: 100%;
    display: block;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}

.clearfix:after {
    clear: both
}


.demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
