<template>
    <div>
        <form id="search">
            Search
            <input name="query" v-model="query">
        </form>
        <ul>
            <li v-for="item in filteredData">
                <span>{{item.date}}</span>
            </li>
        </ul>
        <el-radio-group v-model="radio5">
            <el-radio-button label="上海">
                <img src="http://img06.tooopen.com/images/20160921/tooopen_sy_179583447187.jpg" width="50" height="50x">
            </el-radio-button>
            <el-radio-button label="北京">
                 <img src="http://img06.tooopen.com/images/20160921/tooopen_sy_179583447187.jpg" width="50" height="50x">
            </el-radio-button>
            <el-radio-button label="广州">
                 <img src="http://img06.tooopen.com/images/20160921/tooopen_sy_179583447187.jpg" width="50" height="50x">
            </el-radio-button>
            <el-radio-button label="深圳">
                 <img src="http://img06.tooopen.com/images/20160921/tooopen_sy_179583447187.jpg" width="50" height="50x">
            </el-radio-button>
        </el-radio-group>
    </div>
</template>
<script>
// import {
//     ceshi
// } from '@/service/api'

/* eslint-disable */
export default {
    data() {
            return {
                tableData: [{
                    date: '2016-05-02'
                }, {
                    date: '2016-05-04'
                }, {
                    date: '2016-05-01'
                }, {
                    date: '2016-05-03'
                }],
                value: '',
                query: '',
                radio3: '上海',
                radio4: '上海',
                radio5: '上海'
            }
        },
        computed: {
            filteredData() {
                var query = this.query && this.query.toLowerCase()
                var data = this.tableData
                if (query) {
                    data = data.filter(function(row) {
                        return Object.keys(row).some(function(key) {
                            return String(row[key]).toLowerCase().indexOf(query) > -1
                        })
                    })
                }
                return data
            }
        },
        mounted() {
            // ceshi({
            //     username: 'keda',
            //     password: 'keda'
            // }).then((res) => {
            //     console.log(res)
            // }).catch((err) => {
            //     console.log(err)
            // })
            
            
        }
}
</script>
<style>
.cell-edit-input .el-input,
.el-input__inner {
    width: 100px;
}

.cell-icon {
    cursor: pointer;
    color: #fff;
}
</style>
