<template>
    <div class="wapper">
        <div class="main-top">
            <Headers></Headers>
        </div>
        <div class="main-left" :class="isOpen ? 'showleft' : 'hideleft'">
            <Menus backEndMenu="true"></Menus>
            <div class="menusIcon" @click="menuIsOpen">
                <h3>焊机设备信息化管理平台</h3>
                <i class="iconfont icon-santiaogang"></i>
            </div>
        </div>
        <div class="marin-right">
            <div class="right-waper">
                <transition enter-active-class="animated bounceInUp">
                    <router-view></router-view>
                </transition>
            </div>
        </div>
    </div>
</template>
<script>
import Headers from '@/components/Headers'
import Menus from '@/components/Menu'
export default {
    data() {
        return {
            msg: 'zhouxin',
            theme3: 'light',
            isOpen: false
        }
    },
    methods: {
        resize() {
            if (document.body.clientWidth > 768) {
                this.isOpen = true
            } else {
                this.isOpen = false
            }
            window.onresize = (ev) => {
                if (document.body.clientWidth > 768) {
                    this.isOpen = true
                } else {
                    this.isOpen = false
                }
            }
        },
        menuIsOpen() {
            this.isOpen = !this.isOpen
            console.log(this.isOpen)
        }
    },
    mounted() {
        this.resize()
    },
    components: {
        Headers,
        Menus
    }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
