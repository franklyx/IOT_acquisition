<template>
    <div>
        <el-row>
            <el-col :span="24">
                <el-card class="box-card">
                    <div slot="header" class="clearfix">
                        <el-input placeholder="请选择日期" icon="search" v-model="query">
                        </el-input>
                    </div>
                    <div v-for="item in filteredData" :key="item._id" class="text">
                        <!-- <router-link :to="{path:'/index',query:{id:item._id}}"></router-link> -->
                        <p @click="selectFactory(item._id)">{{item.name}}</p>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>
<script>
import { getFactory } from '@/service/api'
import { mapGetters } from 'vuex'

export default {
    data() {
        return {
            query: '',
            data: []
        }
    },
    computed: {
        filteredData() {
            var query = this.query && this.query.toLowerCase()
            var data = this.data
            if (query) {
                data = data.filter(function(row) {
                    return Object.keys(row).some(function(key) {
                        return String(row[key]).toLowerCase().indexOf(query) > -1
                    })
                })
            }
            return data
        },
        ...mapGetters(['getToken'])
    },
    mounted() {
        // console.log('工厂页面获取token',this.getToken)
        getFactory({
            page: 1,
            per_page: 99999
        }).then(res => {
            if (res.data !== '') {
                this.data = res.data
            }
        })
    },
    methods: {
        selectFactory(id) {
            this.$store.dispatch('selectFactory', id)
            this.$router.push({
                path: '/index',
                query: {
                    id: id
                }
            })
        }
    }
}
</script>

<style lang="scss" scoped>
.text {
    line-height: 30px;
    font-size: 16px;
    cursor: pointer;
    text-align: center;
    &:hover {
        color: red
    }
}
</style>
