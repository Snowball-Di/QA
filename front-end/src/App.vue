<template>
  <el-container>
    <el-header>
      <el-card class="head">
        <span class="title">📣QA System</span>

        <el-tag>
          <router-link to="/Qas">问答(Qustions) | </router-link>
          <router-link to="/">功能(Functions)</router-link>
        </el-tag>
      </el-card>
    </el-header>
    <live2d
      :className="icons"
      ref="live2d"
      style="z-index: 10"
      @click.native="touch"
    ></live2d>
    <el-container>
      <el-aside width="300px">
        <br />
        <br />
        <el-row
          ><div
            style="
              text-align: center;
              font-size: 14px;
              font-weight: bold;
              margin-bottom: 10px;
            "
          >
            摄像头
          </div>
          <video id="video" width="300" height="225"></video>
          <div class="iCenter"></div>
        </el-row>

        <el-row
          ><div
            style="
              text-align: center;
              font-size: 14px;
              font-weight: bold;
              margin-bottom: 10px;
            "
          >
            拍摄效果
          </div>
          <!-- 这里是点击拍照显示的图片画面 -->
          <canvas
            id="photo"
            width="300"
            height="225"
            style="display: block"
          ></canvas>
          <el-button
            class="photobtn"
            type="primary"
            size="small"
            icon="el-icon-news"
            @click="opencamera()"
            style="margin-top: 10px; text-align: center"
            >权限</el-button
          >
          <el-button
            class="photobtn"
            type="primary"
            size="small"
            icon="el-icon-camera"
            @click="takephoto()"
            style="margin-top: 10px; text-align: center"
            >拍照</el-button
          >
          <el-button
            class="photobtn"
            type="primary"
            size="small"
            icon="el-icon-view"
            @click="uploadphoto()"
            style="margin-top: 10px; text-align: center"
            >识别</el-button
          >
          <br />
          <br />
          <canvas id="canvas" style="height: 50px; width: 150px"></canvas>
        </el-row>
      </el-aside>
      <el-main>
        <transition name="fade-transform" mode="out-in">
          <keep-alive>
            <router-view
              @girlmessage="girlmessage"
              @girlsay="girlsay"
            ></router-view>
          </keep-alive>
        </transition>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { sendphoto } from "@/api";
import { AppID } from "./config.json";
import { API_key } from "./config.json";
import { Secret_Key } from "./config.json";

export default {
  name: "app",
  data() {
    return {
      AipSpeechClient: null,
      client: null,
      icons: [],
      loadingbut: false,
      preViewVisible: false,
      blobFile: null,
      photo: null,
      video: null,
      mediaStreamTrack: "",
      faceResponse: [
        "我看到了一个人，那是你吗？",
        "我想你可以多笑一笑~",
        "你在发呆吗，能告诉我你在想什么吗？",
        "如果我能从这里出去的话，我想我会去找你的:)",
        "我记住你的样子了，你也别忘了我哦~",
        "我想我可以换一件衣服...",
      ],
      touchResponse: [
        "喜欢我也不可以乱摸哦~",
        "你手放在那儿干什么，快给我拿开~",
        "再这样我可就生气 TT 哼！",
        "这样是不对的，不对的...",
      ],
    };
  },
  mounted() {
    this.video = document.getElementById("video");
    this.photo = document.getElementById("photo");
  },
  methods: {
    girlsay(text) {
      var APP_ID = AppID;
      var API_KEY = API_key;
      var SECRET_KEY = Secret_Key;
      var AipSpeechClient = require("baidu-aip-sdk").speech;
      var client = new AipSpeechClient(APP_ID, API_KEY, SECRET_KEY);
      client.text2audio(text, { spd: 0, per: 4 }).then(
        function (result) {
          if (result.data) {
            fs.writeFileSync("tts.mpVoice.mp3", result.data);
            let audio = new Audio();
            audio.src = "tts.mpVoice.mp3";
            audio.play();
          } else {
            // 服务发生错误
            console.log(result);
          }
        },
        function (e) {
          // 发生网络错误
          console.log(e);
        }
      );
    },

    girlmessage(text) {
      this.$refs.live2d.showMessage(text, 3000, 1000);
    },
    touch() {
      let index = Math.ceil(Math.random() * 10) % 4;
      let m = this.touchResponse[index];
      this.$refs.live2d.showMessage(m, 3000, 1000);
      // this.girlsay(m);
    },
    opencamera() {
      var video = document.querySelector("video");

      if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {};
      }
      if (navigator.mediaDevices.getUserMedia === undefined) {
        navigator.mediaDevices.getUserMedia = function (constraints) {
          var getUserMedia =
            navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia ||
            navigator.msGetUserMedia;
          if (!getUserMedia) {
            return Promise.reject(
              new Error("getUserMedia is not implemented in this browser")
            );
          }
          return new Promise(function (resolve, reject) {
            getUserMedia.call(navigator, constraints, resolve, reject);
          });
        };
      }

      //摄像头调用配置
      var mediaOpts = {
        audio: false,
        video: true,
      };

      let that = this;
      navigator.mediaDevices
        .getUserMedia(mediaOpts)
        .then(function (stream) {
          that.mediaStreamTrack = stream;
          video = document.querySelector("video");
          if ("srcObject" in video) {
            video.srcObject = stream;
          } else {
            video.src =
              (window.URL && window.URL.createObjectURL(stream)) || stream;
          }
          video.play();
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    dataURLtoBlob(dataurl) {
      var arr = dataurl.split(","),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]),
        n = bstr.length,
        u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new Blob([u8arr], { type: mime });
    },
    takephoto() {
      //点击拍照截图画面
      let that = this;
      that.photo.getContext("2d").drawImage(this.video, 0, 0, 300, 225);
      let dataurl = that.photo.toDataURL("image/jpeg", 1.0);
      that.blobFile = this.dataURLtoBlob(dataurl);
      that.preViewVisible = true;
    },
    uploadphoto() {
      if (!this.blobFile) return;
      else {
        sendphoto(this.blobFile)
          .then((res) => {
            if (!res.data.code) {
              if (res.data.results) {
                console.log(res.data.results);
                // TODO 接入虚拟形象行为
                let index = Math.ceil(Math.random() * 10) % 5;
                let m = this.faceResponse[index];
                this.$refs.live2d.showMessage(m, 3000, 1000);

                if (index > 1) {
                  this.$refs.live2d.showMessage(
                    this.faceResponse[5],
                    2000,
                    1000
                  );
                  this.$refs.live2d.loadRandModel();
                }
              } else {
                this.$refs.live2d.showMessage(
                  "并没有看见你的人呢，也许你并不喜欢我呢:(",
                  3000,
                  1000
                );
                this.$refs.live2d.loadOtherModel();
                console.log(res.data.results);
              }
            }
          })
          .catch(() => {
            this.$refs.live2d.showMessage(
              "我想系统可能发生了一些错误，检查一下网络吧~",
              3000,
              1000
            );
          });
      }
    },
  },
  components: {},
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
.el-container {
  width: 1000px;
  position: relative;
  margin: 0 auto;
  flex-direction: column;
}
.el-row {
  text-align: center;
}

.el-tag {
  position: relative;
  margin-left: 20px;
  font-size: 14px;
}

.head {
  margin: 0 auto;
  position: relative;
}
</style>
