<template>
    <div class="login">
        <div class="container">
            <div class="content">
                <div id="large-header" class="login_bd base">
                    <canvas id="demo-canvas"></canvas>
                    <div class="pro_login base  animated zoomInUp">
                        <div id="loginForm" class="login_form">
                            <div class="login_text">
                                <span class="code_login">账号登录</span>
                                <!-- <a href="/CAS" class="other_login">CAS登录</a>  -->
                            </div>
                            <div class="login_info clearfix">
                                <input type="text" class="lg_input username" :class="{lg_blur:loginForm.username.length !==0}" autocomplete="off" v-model="loginForm.username" />
                                <label class="lg_lable">
                                    账号
                                </label>
                            </div>
                            <div class="login_info clearfix ">
                                <input type="password" class="lg_input password" :class="{lg_blur:loginForm.password.length !==0}" autocomplete="off" v-model="loginForm.password" @keydown.enter="loginFn" />
                                <label class="lg_lable">
                                    密码
                                </label>
                            </div>
                            <div class="l_ts" id="hint" v-show="msg">{{msg}}</div>
                            <div class="loginBtn ">
                                <input type="button" value="登录" id="login" class="login_btn" @click="loginFn" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {
    sysInit
} from '@/service/api'
export default {
    data() {
        return {
            loginForm: {
                username: '',
                password: ''
            },
            msg: '',
            lg_blur: false
        }
    },
    beforeCreate() {
        sysInit().then(res => {
            if (res.data === 'False') {
                this.$router.push('/facInit')
            }
        })
    },
    mounted() {
        this.bgFn()
    },
    methods: {
        loginFn() {
            this.$store.dispatch('login', this.loginForm).then((res) => {
                if (res.code === 201) {
                    this.msg = ''
                    // this.$store.dispatch('selectFactory', res.data.factory_id)
                    this.$router.push('/factory')
                } else {
                    this.msg = '账户名密码错误'
                }
            }).catch(err => {
                console.log(err)
            })
        },
        // 雪花特效
        bgFn() {
            (function() {
                var lastTime = 0;
                var vendors = ['ms', 'moz', 'webkit', 'o'];
                for (var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
                    window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
                    window.cancelAnimationFrame = window[vendors[x] + 'CancelAnimationFrame'] ||
                        window[vendors[x] + 'CancelRequestAnimationFrame'];
                }
                if (!window.requestAnimationFrame) {
                    window.requestAnimationFrame = function(callback, element) {
                        var currTime = new Date().getTime();
                        var timeToCall = Math.max(0, 16 - (currTime - lastTime));
                        var id = window.setTimeout(function() {
                            callback(currTime + timeToCall);
                        },
                            timeToCall);
                        lastTime = currTime + timeToCall;
                        return id;
                    };
                }
                if (!window.cancelAnimationFrame) {
                    window.cancelAnimationFrame = function(id) {
                        clearTimeout(id);
                    };
                }
                var width, height, largeHeader, canvas, ctx, circles, animateHeader = true;
                initHeader();
                addListeners();

                function initHeader() {
                    width = window.innerWidth;
                    height = window.innerHeight;
                    largeHeader = document.getElementById('large-header');
                    largeHeader.style.height = height + 'px';
                    canvas = document.getElementById('demo-canvas');
                    canvas.width = width;
                    canvas.height = height;
                    ctx = canvas.getContext('2d');
                    // create particles
                    circles = [];
                    for (var x = 0; x < width * 0.5; x++) {
                        var c = new Circle();
                        circles.push(c);
                    }
                    animate();
                }

                // Event handling
                function addListeners() {
                    window.addEventListener('scroll', scrollCheck);
                    window.addEventListener('resize', resize);
                }

                function scrollCheck() {
                    if (document.body.scrollTop > height) animateHeader = false;
                    else animateHeader = true;
                }

                function resize() {
                    width = window.innerWidth;
                    height = window.innerHeight;
                    largeHeader.style.height = height + 'px';
                    canvas.width = width;
                    canvas.height = height;
                }

                function animate() {
                    if (animateHeader) {
                        ctx.clearRect(0, 0, width, height);
                        for (var i in circles) {
                            circles[i].draw();
                        }
                    }
                    requestAnimationFrame(animate);
                }

                // Canvas manipulation
                function Circle() {
                    var _this = this;
                    // constructor
                    (function() {
                        _this.pos = {}
                        init();
                    })();

                    function init() {
                        _this.pos.x = Math.random() * width;
                        _this.pos.y = height + Math.random() * 100;
                        _this.alpha = 0.1 + Math.random() * 0.3;
                        _this.scale = 0.1 + Math.random() * 0.3;
                        _this.velocity = Math.random();
                    }
                    this.draw = function() {
                        if (_this.alpha <= 0) {
                            init();
                        }
                        _this.pos.y -= _this.velocity;
                        _this.alpha -= 0.0005;
                        ctx.beginPath();
                        ctx.arc(_this.pos.x, _this.pos.y, _this.scale * 10, 0, 2 * Math.PI, false);
                        ctx.fillStyle = 'rgba(255,255,255,' + _this.alpha + ')';
                        ctx.fill();
                    };
                }
            })();
        }
    }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
body {
    font-family: "微软雅黑";
    overflow: hidden;
}

* {
    padding: 0;
    margin: 0;
}

a {
    text-decoration: none;
}

*::before,
*::after {
    -webkit-box-sizing: inherit;
    -moz-box-sizing: inherit;
    box-sizing: inherit;
}

.clearfix::before,
.clearfix::after {
    display: table;
    content: '';
}

.base {
    display: -webkit-box;
    display: -moz-box;
    display: -webkit-flex;
    display: flex;
    align-items: center;
    -webkit-align-items: center;
    -ms-align-items: center;
    justify-content: space-around;
    -webkit-justify-content: space-around;
}

.login_bd {
    flex-direction: column;
    -webkit-flex-direction: column;
    position: absolute;
    width: 100%;
    top: 0;
    height: 100%;
    min-height: 500px;
    background: url("./../assets/images/proLogin.png") no-repeat 50% 50%;
}

.pro_login {
    -webkit-box-flex: 1;
    -moz-box-flex: 1;
    -webkit-flex: 1;
    flex: 1;
    min-height: 300px;
    position: absolute;
    top: 50%;
    margin-top: -196px;
    left: 50%;
    margin-left: -142px;
    // animation-delay: .5s;
}

.login_text {
    height: 35px;
    line-height: 35px;
    position: relative;
    border-bottom: 1px solid #5182e4;
    color: #fff;
    font-size: 18px;
}

.other_login {
    width: 60px;
    height: 25px;
    line-height: 25px;
    background-color: #5182e4;
    border-radius: 4px;
    display: inline-block;
    float: right;
    font-size: 12px;
    text-align: center;
    color: #fff;
}

.login_form {
    position: relative;
    padding: 10px;
    width: 270px;
    margin: 0 auto;
    z-index: 100;
}

.login_info {
    height: 60px;
    position: relative;
}

.lg_input {
    position: absolute;
    bottom: 0;
    left: 0;
    box-sizing: border-box;
    width: 100%;
    height: 28px;
    line-height: 28px;
    color: #fff;
    border: 0;
    font-size: 14px;
    font-weight: 400;
    background: 0 0;
    box-shadow: inset 0 -1px 0 0 rgba(81, 130, 228, 1);
    z-index: 2;
}

.lg_input:focus {
    box-shadow: inset 0 -2px 0 0 rgba(81, 130, 228, 1);
}

.lg_lable {
    position: absolute;
    left: 0;
    bottom: 0;
    font-size: 16px;
    height: 28px;
    line-height: 28px;
    transition: .2s ease all;
    color: rgba(255, 255, 255, .6);
    z-index: 1;
}

.l_ts {
    height: 35px;
    line-height: 35px;
    color: #e45151;
    font-size: 12px;
    margin-top: 10px;
    // visibility: hidden;
}

.login_btn {
    width: 100%;
    text-align: center;
    height: 40px;
    line-height: 40px;
    display: inline-block;
    color: #fff;
    font-size: 14px;
    border-radius: 0;
    cursor: pointer;
    background: #5182E4;
    border: 0;
    position: relative;
    z-index: 999;
    margin-top: 10px;
    transition: all .2s ease-in-out;
}

.login_btn:hover {
    background: #4e7cd9;
}

.lg_input:focus {
    outline: none;
}

.lg_input:focus + .lg_lable {
    position: absolute;
    bottom: 22px;
    font-size: 14px;
    color: #5182e4;
    transition: all 0.2s ease 0s;
}

.lg_blur +.lg_lable {
    color: rgba(255, 255, 255, .6);
}

.lg_blur + .lg_lable {
    position: absolute;
    bottom: 22px;
    font-size: 14px;
    color: rgba(255, 255, 255, .6);
    transition: .2s ease all;
}
</style>
