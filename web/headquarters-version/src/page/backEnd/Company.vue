<template>
    <div>
        <!-- <el-form :inline="true" :model="formInline" class="demo-form-inline" @submit.native.prevent>
            <el-form-item label="公司名称">
                <el-input v-model="formInline.name" placeholder="公司名称" @keyup.enter.native="addFactoryFn"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addFactoryFn">添加</el-button>
            </el-form-item>
        </el-form> -->
        <div class="table-box">
            <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="name" label="公司名称" align="center"></el-table-column>
                <el-table-column label="操作" v-if="isFormStatus" align="center">
                    <template scope="scope">
                        <el-button type="text" size="small" @click="openDialog(scope.$index,scope.row)">编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="dialog-box">
            <el-dialog title="编辑" :visible.sync="dialogFormVisible" size="tiny">
                <el-form>
                    <el-form-item label="用户名" :label-width="formLabelWidth">
                        <el-input v-model="editRow.name" auto-complete="off" @keyup.enter.native="modifyFactoryFn"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="modifyFactoryFn">确 定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
import {
    mapGetters
} from 'vuex'
import {
    getFactory,
    modifyFactory
} from '@/service/api'
export default {
    mounted() {
        this.initFactory()
    },
    computed: {
        ...mapGetters(['isFormStatus'])
    },
    methods: {
        initFactory() {
            const loading = this.$loading({
                target: '.table-box',
                text: '拼命加载中'
            })
            getFactory({
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
        modifyFactoryFn() {
            modifyFactory({
                factory_id: this.editRow['_id'],
                name: this.editRow.name
            }).then(res => {
                if (res.code === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2 * 1000
                    })
                    this.initFactory();
                    this.dialogFormVisible = false
                }
            })
        },
        openDialog(index, rows) {
            this.editRow = rows
            this.dialogFormVisible = true
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
            editRow: {}
        }
    }
}
</script>
<style>
</style>
