<template>
    <div class="dev-config">
        <el-form :model="form" ref="form" label-width="80px">
            <el-form-item label="类别" prop="name">
                <el-input v-model="form.name" placeholder="类别"></el-input>
            </el-form-item>
            <el-form-item label="产品型号" prop="product_number">
                <el-input v-model="form.product_number" placeholder="产品型号"></el-input>
            </el-form-item>
            <el-form-item label="设备图片" prop="pic_url">
                <el-radio-group v-model="form.pic_url">
                    <el-radio-button  v-for="item in radioList" :label="item.url" :key="item.id">
                        <div class="bgimg"  v-bind:style="{backgroundImage:'url(http://'+getBaseUrl+''+item.url+')'}"></div>
                    </el-radio-button>
                </el-radio-group>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addProductFn">添加</el-button>
            </el-form-item>
            </el-form-item>
        </el-form>
       


       <div class="table-box">
           <el-table :data="tableData" style="width: 100%">
               <el-table-column  :key="tableData.name" align="center" min-width="150" prop="name" label="类别"></el-table-column>
               <el-table-column  :key="tableData.number" align="center" min-width="150" prop="number" label="产品型号" ></el-table-column>
               <el-table-column  align="center" min-width="150" label="图片" >
                   <template scope="scope">
                        <!-- <span>asdsad</span> -->
                        <div class="smallbg-img" v-bind:style="{backgroundImage:'url(http://'+getBaseUrl+''+scope.row.mini_pic_url+')'}"></div>
                   </template>
               </el-table-column>
               <el-table-column label="操作" align="center" min-width="150">
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
                       <el-form-item label="类别" :label-width="formLabelWidth">
                           <el-input v-model="editRow.name" auto-complete="off"></el-input>
                       </el-form-item>
                     </el-col>
                   </el-row>
                   </el-form-item>
                   <el-form-item label="产品型号" :label-width="formLabelWidth">
                       <el-input v-model="editRow.number" auto-complete="off"></el-input>
                   </el-form-item>
                   <el-form-item label="设备图片" :label-width="formLabelWidth">
                       <el-radio-group v-model="editRow.pic_url">
                           <el-radio-button label="上海" v-for="item in radioList" :label="item.url" :key="item.id">
                               <div class="bgimg"  v-bind:style="{backgroundImage:'url(http://'+getBaseUrl+''+item.url+')'}"></div>
                           </el-radio-button>
                       </el-radio-group>
                   </el-form-item>
               </el-form>
               <div slot="footer" class="dialog-footer">
                   <el-button @click="dialogFormVisible = false">取 消</el-button>
                   <el-button type="primary" @click="modifyProductFn">确 定</el-button>
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
   getPicUrl,
   getProductList,
   addProduct,
   modifyProduct,
   deleteProduct
} from '@/service/api'

export default {
    mounted() {
        this.initData()
        this.getPicUrlFn()
    },
    computed: {
        ...mapGetters(['isFormStatus', 'getFactoryId', 'getBaseUrl'])
    },
    methods: {
        openDialog(index, rows) {
            console.log(rows)
            this.editRow = rows
            this.dialogFormVisible = true
        },
        initData() {
            getProductList({
                factory_id: this.getFactoryId,
                page: 1,
                per_page: 99999
            }).then(res => {
                if (res.code === 201) {
                    this.tableData = res.data
                }
            })
        },
        getPicUrlFn() {
            getPicUrl().then(res => {
                if (res.code === 200) {
                    this.radioList = res.data
                }
            })
        },
        addProductFn() {
            addProduct({
                factory_id: this.getFactoryId, name: this.form.name, product_number: this.form.product_number, pic_url: this.form.pic_url
            }).then(res => {
                if (res.code === 201) {
                    this.$message({
                        type: 'success',
                        message: '添加成功!',
                        duration: 2 * 1000
                    })
                    this.initData()
                    this.$refs['form'].resetFields()
                } else if (res.code === 400) {
                    this.$message({
                        type: 'warning',
                        message: '不可重复添加!',
                        duration: 2 * 1000
                    })
                }
            })
        },
        modifyProductFn() {
            modifyProduct({
                factory_id: this.getFactoryId, product_id: this.editRow['_id'], name: this.editRow['name'], product_number: this.editRow['number'], pic_url: this.editRow['pic_url']
            }).then(res => {
                if (res.code === 200) {
                    this.dialogFormVisible = false
                    this.initData()
                } else if (res.code === 400) {
                    this.$message({
                        type: 'warning',
                        message: '不可重复添加!',
                        duration: 2 * 1000
                    })
                }
            })
        },
        deleteRow(index, rows) {
            deleteProduct({
                factory_id: this.getFactoryId, product_id: rows['_id']
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
            form: {
                name: '',
                number: '',
                pic_url: ''
            },
            tableData: [],
            dialogFormVisible: false,
            formLabelWidth: '100px',
            radioList: [],
            editRow: {}
        }
    }
}
</script>
<style lang="scss">
.dev-config .el-radio-button__inner{
    padding: 3px 3px;
}
.dev-config .bgimg{
    width: 50px;
    height: 50px;
    background-size: cover;
    background-position:center center;
    background-repeat: no-repeat;
}
.dev-config .smallbg-img{
    width: 20px;
    height: 20px;
    display: inline-block;
    background-size: cover;
    background-position:center center;
    background-repeat: no-repeat;
}

</style>
