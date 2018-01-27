<template>
    <div>
        <el-form :inline="true" :model="formInline" :rules="rules" ref="formInline" class="demo-form-inline" @submit.native.prevent>
            <el-form-item label="班组名称" prop="selectGroup">
                <el-select v-model="formInline.selectGroup" placeholder="班组名称" @change="changeGroup">
                    <el-option v-for="item in groupList" :key="item._id" :label="item.name" :value="item._id">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="班次名称" prop="name">
                <el-input v-model="formInline.name" placeholder="班次名称"></el-input>
            </el-form-item>
            <el-form-item label="开始时间" prop="start_time">
                <el-time-select
                    placeholder="起始时间"
                    v-model="formInline.start_time"
                    :picker-options="{
                      start: '08:30',
                      step: '00:15',
                      end: '18:30'
                    }">
                </el-time-select>
            </el-form-item>
            <el-form-item label="结束时间" prop="end_time">
                <el-time-select
                    placeholder="结束时间"
                    v-model="formInline.end_time"
                    :picker-options="{
                      start: '08:30',
                      step: '00:15',
                      end: '18:30',
                      minTime: formInline.start_time
                    }">
                  </el-time-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addWorkScheduleFn">添加</el-button>
            </el-form-item>
        </el-form>
        <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="name" align="center" min-width="150" label="班次名称"></el-table-column>
            <el-table-column prop="workgroup_name" align="center" min-width="150" label="班组名称"></el-table-column>
            <el-table-column prop="start_time" align="center" min-width="150" label="开始时间"></el-table-column>
            <el-table-column prop="end_time" align="center" min-width="150" label="结束时间"></el-table-column>
            <el-table-column align="center" min-width="150" label="搓作">
                <template scope="scope">
                    <el-button type="text" size="small" @click="openDialog(scope.$index,scope.row)">编辑</el-button>
                    <el-button @click="deleteRow(scope.$index,scope.row)" type="text">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <div class="dialog-box">
            <el-dialog title="编辑" :visible.sync="dialogFormVisible" size="tiny">
                <el-form>
                    <el-form-item label="班次名称" :label-width="formLabelWidth">
                        <el-input v-model="editRow.name" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="开始时间" :label-width="formLabelWidth">
                         <el-time-select
                             placeholder="起始时间"
                             v-model="editRow.start_time"
                             :picker-options="{
                               start: '08:30',
                               step: '00:15',
                               end: '18:30'
                             }">
                         </el-time-select>
                    </el-form-item>
                    <el-form-item label="结束时间" :label-width="formLabelWidth">
                        <el-time-select
                            placeholder="结束时间"
                            v-model="editRow.end_time"
                            :picker-options="{
                              start: '08:30',
                              step: '00:15',
                              end: '18:30',
                              minTime: formInline.start_time
                            }">
                          </el-time-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="modifyWorkScheduleFn">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
import {
    getWorkGroup,
    getWorkSchedule,
    addWorkSchedule,
    modifyWorkSchedule,
    deleteWorkSchedule
} from '@/service/api'
import {
    mapGetters
} from 'vuex'
export default {
    computed: {
        ...mapGetters(['getFactoryId'])
    },
    mounted() {
        this.initGroup()
        this.initWorkSchedule()
    },
    methods: {
        initGroup() {
            getWorkGroup({
                factory_id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.code === 201) {
                    this.groupList = res.data
                }
            })
        },
        initWorkSchedule() {
            getWorkSchedule({
                factory_id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.code === 201) {
                    this.tableData = res.data
                }
            })
        },
        addWorkScheduleFn() {
            this.$refs['formInline'].validate((valid) => {
                if (valid) {
                    addWorkSchedule({
                        factory_id: this.getFactoryId,
                        name: this.formInline.name,
                        group_id: this.formInline.selectGroup,
                        start_time: this.formInline.start_time,
                        end_time: this.formInline.end_time
                    }).then(res => {
                        if (res.code === 201) {
                            this.$message({
                                type: 'success',
                                message: '添加成功!',
                                duration: 2 * 1000
                            })
                            this.initWorkSchedule()
                            this.$refs['formInline'].resetFields()
                        }
                    })
                }
            })
        },
        modifyWorkScheduleFn() {
            console.log(this['editRow'])
            modifyWorkSchedule({
                factory_id: this.getFactoryId,
                schedule_id: this['editRow']['_id'],
                group_id: this['editRow']['group_id'],
                name: this['editRow']['name'],
                start_time: this['editRow']['start_time'],
                end_time: this['editRow']['end_time']
            }).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2 * 1000
                    })
                    this.initWorkSchedule()
                    this.dialogFormVisible = false
                }
            })
        },
        deleteRow(index, rows) {
            deleteWorkSchedule({
                factory_id: this.getFactoryId,
                schedule_id: rows['_id']
            }).then(res => {
                if (res.code === 204) {
                    this.$message({
                        type: 'success',
                        message: '删除成功!',
                        duration: 2 * 1000
                    })
                    this.initWorkSchedule()
                }
            })
        },
        openDialog(index, rows) {
            this.editRow = rows
            this.dialogFormVisible = true
        },
        changeGroup() {

        }
    },
    data() {
        return {
            groupList: [],
            formInline: {
                name: '',
                selectGroup: '',
                start_time: '',
                end_time: ''
            },
            value1: '',
            tableData: [],
            dialogFormVisible: false,
            form: {
                name: '',
                region: '',
                date1: '',
                date2: '',
                delivery: false,
                type: [],
                resource: '',
                desc: ''
            },
            formLabelWidth: '100px',
            editRow: {},
            rules: {
                name: [{
                    required: true,
                    message: '请输入内容',
                    trigger: 'blur'
                }]
            }

        }
    }
}
</script>
<style>
</style>
