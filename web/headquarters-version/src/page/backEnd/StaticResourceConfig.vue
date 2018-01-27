<template>
    <div>
        <el-upload action="/api/v1/upload-file" list-type="picture-card" :file-list="fileList2" :multiple="true" :data="form" :headers="headerData" :on-preview="handlePictureCardPreview" :before-upload="beforeUpload" :on-success="successFn" :on-error="errorFn" :on-progress="progress" :on-remove="handleRemove">
            <i class="el-icon-plus"></i>
        </el-upload>
        <el-dialog v-model="dialogVisible" size="tiny">
            <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>
    </div>
</template>
<script>
import {
    getPicUrl,
    deletePicUrl
} from '@/service/api'
import {
    mapGetters
} from 'vuex'
export default {
    data() {
        return {
            dialogImageUrl: '',
            dialogVisible: false,
            headerData: {
                token: ''
            },
            fileList2: [],
            form: {}
        };
    },
    created() {
        getPicUrl().then(res => {
            if (res.code === 200) {
                console.log(res.data)
                this.fileList2 = res.data
            }
        })
    },
    computed: {
        ...mapGetters(['getToken'])
    },
    methods: {
        beforeUpload(file) {
            this.headerData.token = this.getToken
            return file
        },
        handleRemove(file, fileList) {
            deletePicUrl({
                file_name: file.name
            }).then(res => {
                if (res.code === 204) {
                    this.$message({
                        type: 'success',
                        message: '删除成功!',
                        duration: 2 * 1000
                    })
                }
            })
        },
        handlePictureCardPreview(file) {
            console.log(file)
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },
        successFn(response, file, fileList) {
            if (file.response.code === 201) {
                this.$message({
                    type: 'success',
                    message: '上传成功!',
                    duration: 2 * 1000
                })
                return false
            }
        },
        errorFn(response, file, fileList) {
            console.log('error')
        },
        progress(event, file, fileList) {}
    }
}
</script>
<style scoped>
</style>
