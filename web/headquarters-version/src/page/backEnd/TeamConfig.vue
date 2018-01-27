<template>
    <div>
        <el-form :model="formInline" :inline='true' label-width="80px" @submit.native.prevent class="from-box" v-if="isFormStatus">
            <el-form-item label="班组名称">
                <el-input v-model="formInline.name" placeholder="班组名称" @keyup.enter.native="addWorkGroupFN" style="width:200px"></el-input>
            </el-form-item>
            <!-- <el-form-item label="设备">
                <el-select v-model="equipment_list" multiple placeholder="请选择">
                    <el-option
                     v-for="item in deciveList"
                     :key="item._id"
                     :label="item.name"
                     :value="item._id">
                    </el-option>
                </el-select>
            </el-form-item> -->
            <el-form-item label="选择设备">
                <el-checkbox-group v-model="equipment_list">
                    <el-checkbox name="type" v-for="item in deciveList" :key="item._id" :label="item._id">{{item.name}}</el-checkbox>
                </el-checkbox-group>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addWorkGroupFN">添加</el-button>
            </el-form-item>
        </el-form>
        <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="name" align="center" min-width="150" label="班组名称"></el-table-column>
            <el-table-column align="center" min-width="150" label="设备">
                <template scope="scope">
                   <span v-for="item in scope.row.equipments">{{item.name}},</span>
                </template>
            </el-table-column>
            <el-table-column align="center" min-width="150" label="操作" v-if="isFormStatus">
                <template scope="scope">
                    <el-button type="text" size="small" @click="openDialog(scope.$index,scope.row)">编辑</el-button>
                    <el-button @click="deleteRow(scope.$index,scope.row)" type="text">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <div class="dialog-box">
            <div class="dialg-box">
                <el-dialog title="编辑" :visible.sync="dialogFormVisible" size="tiny">
                    <el-form @submit.native.prevent>
                        <el-form-item label="班组" :label-width="formLabelWidth">
                            <el-input v-model="editRow.name" auto-complete="off"></el-input>
                        </el-form-item>
                        <el-form-item label="选择设备" :label-width="formLabelWidth">
                            <el-checkbox-group v-model="editRow.equipment_list">
                                 <el-checkbox name="type" v-for="item in deciveList" :key="item._id" :label="item._id">{{item.name}}</el-checkbox>
                            </el-checkbox-group>
                        </el-form-item>
                    </el-form>
                    <div slot="footer" class="dialog-footer">
                        <el-button @click="dialogFormVisible = false">取 消</el-button>
                        <el-button type="primary" @click="modifyWorkGroupFn">确 定</el-button>
                    </div>
                </el-dialog>
            </div>
        </div>
    </div>
</template>
<script>
import {
    getWorkGroup,
    addWorkGroup,
    modifyWorkGroup,
    deleteWorkGroup,
    getDevice
} from '@/service/api'
import {
    mapGetters
} from 'vuex'
let cityOptions = []
export default {
    computed: {
        ...mapGetters(['getFactoryId', 'isFormStatus'])
    },
    mounted() {
        this.initDevice()
        this.initWorkGroup()
    },
    methods: {
        initWorkGroup() {
            getWorkGroup({
                factory_id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.code === 201) {
                    this.tableData = res.data
                }
            })
        },
        addWorkGroupFN() {
            addWorkGroup({
                factory_id: this.getFactoryId,
                name: this.formInline.name,
                equipment_list: this.equipment_list
            }).then(res => {
                if (res.code === 201) {
                    this.$message({
                        type: 'success',
                        message: '添加成功!',
                        duration: 2 * 1000
                    })
                    this.initWorkGroup()
                }
            })
        },
        deleteRow(index, rows) {
            console.log(rows['_id'])
            deleteWorkGroup({
                factory_id: this.getFactoryId,
                group_id: rows['_id']
            }).then(res => {
                if (res.code === 204) {
                    this.$message({
                        type: 'success',
                        message: '删除成功!',
                        duration: 2 * 1000
                    })
                    this.initWorkGroup()
                }
            })
        },
        modifyWorkGroupFn() {
            modifyWorkGroup({
                factory_id: this.getFactoryId,
                group_id: this.editRow._id,
                equipment_list: this.editRow.equipment_list
            }, {
                name: this.editRow
            }).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2 * 1000
                    })
                    this.initWorkGroup()
                    this.dialogFormVisible = false
                }
            })
        },
        openDialog(index, rows) {
            this.editRow = rows
            this.dialogFormVisible = true
        },
        initDevice() {
            // const loading = this.$loading({
            //     target: '.table-box',
            //     text: '拼命加载中'
            // })
            getDevice({
                factory_id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.code === 201) {
                    this.deciveList = res.data
                    cityOptions = res.data
                }
                // loading.close()
            })
        },
        handleCheckAllChange(event) {
            this.checkedCities = event.target.checked ? cityOptions : [];
            this.isIndeterminate = false;
        },
        handleCheckedCitiesChange(value) {
            let checkedCount = value.length;
            this.checkAll = checkedCount === this.cities.length;
            this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length;
        }
    },
    data() {
        return {
            formInline: {
                name: ''
            },
            tableData: [],
            dialogFormVisible: false,
            formLabelWidth: '100px',
            editRow: { },
            deciveList: [],
            equipment_list: []

        }
    }
}
</script>
<style scoped>

</style>
