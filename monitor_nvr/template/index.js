const {createApp} = Vue

createApp({
    data() {
        return {
            message: 'Hello Vue!', items: [], player: null,
        }
    }, mounted() {
        this.init()
    }, methods: {
        init() {
            console.log('hello,world')
            axios({
                method: "post",
                url: "/get/video/url",
                headers: {"x-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6I"},
            }).then(res => {
                if (res.data.err != 200) {
                    alert("错误")
                } else {
                    this.items = res.data.data

                    this.items.forEach((value, key) => {
                        let player = new ckplayer({
                            container: value['video'], //视频容器
                            variable: "player", //该属性必需设置，值等于下面的new chplayer()的对象
                            volume: 0.1,//默认音量，范围0-1
                            live: true,//指定为直播
                            autoplay: true,//自动播放
                            // crossOrigin:'*',//发送跨域信息，示例：Anonymous
                            // playbackrateOpen: true,//不显示倍速菜单
                            plug: 'flv.js',//设置使用flv插件
                            video: value['VideoFlvUrl'],
                        });
                    })
                }
            }).catch(err => {
                console.log(err)
            })
        }
    }
}).mount('#app')