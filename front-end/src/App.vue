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
    <live2d ref="aaa" style="z-index: 10"></live2d>
    <el-container>
      <el-aside width="300px">
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
            <router-view></router-view>
          </keep-alive>
        </transition>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { sendphoto } from "@/api";

export default {
  name: "app",
  data() {
    return {
      loadingbut: false,
      preViewVisible: false,
      blobFile: null,
      photo: null,
      video: null,
      mediaStreamTrack: "",
    };
  },
  mounted() {
    this.video = document.getElementById("video");
    this.photo = document.getElementById("photo");
  },
  methods: {
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
        bstr = Buffer.from(arr[1], "base64"),
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
              console.log(res.data.results);
              // TODO 接入虚拟形象行为

              this.$confirm("你长得真好看啊", "Hello", {
                distinguishCancelAndClose: true,
                confirmButtonText: "是的呢",
                cancelButtonText: "我也这么觉得",
              });
            } else {
              this.$confirm(
                "并没有看见你的人呢，可能出现了一些问题",
                "出现了意外",
                {
                  distinguishCancelAndClose: true,
                  confirmButtonText: "关闭",
                }
              );
              console.log(res.data.results);
            }
          })
          .catch(() => {
            this.messages.push({
              user: 1,
              content: "发生了一些未知错误，稍后再试哦...",
            });
            this.pending = false;
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
