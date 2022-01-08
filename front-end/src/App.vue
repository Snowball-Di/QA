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
    takephoto() {
      //点击拍照截图画面
      let that = this;
      that.photo.getContext("2d").drawImage(this.video, 0, 0, 300, 225);
      let dataurl = that.photo.toDataURL("image/jpeg");
      that.blobFile = that.dataURLtoFile(dataurl, "camera.jpg");
      that.preViewVisible = true;
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
