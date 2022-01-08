  <template>
  <el-card class="qapage">
    <div class="messages" v-chat-scroll="{ always: true, smooth: true }">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="chatbox"
        :class="'user' + message.user"
      >
        {{ message.content }}
      </div>
    </div>

    <el-input
      v-model="input"
      placeholder="请输入你的问题"
      @keyup.enter.native="!pending && sendMessage(input)"
      clearable=""
    >
      <template slot="append">
        <el-button @click="sendMessage(input)" :loading="pending"
          >发送</el-button
        >
      </template>
    </el-input>

    <div class="records-buttons" style="margin: 5px">
      <el-button
        type="success"
        size="medium"
        @click="getPermission()"
        style="margin: 5px"
        >获取麦克权限</el-button
      >
      <el-button
        type="info"
        size="medium"
        @click="startRecorder()"
        style="margin: 5px"
        >开始录音</el-button
      >
      <el-button
        type="info"
        size="medium"
        @click="stopRecorder()"
        style="margin: 5px"
        >结束录音</el-button
      >

      <br />
      <el-button
        type="primary"
        size="medium"
        @click="playRecorder()"
        style="margin: 5px"
        >录音播放</el-button
      >
      <el-button
        type="danger"
        size="medium"
        @click="destroyRecorder()"
        style="margin: 5px"
        >销毁录音</el-button
      >
      <el-button
        type="success"
        size="medium"
        @click="recognize()"
        style="margin: 5px"
        >识别</el-button
      >
    </div>
  </el-card>
</template>

<script>
import { sendMessage } from "@/api";
import { sendAudio } from "@/api";
import Recorder from "js-audio-recorder";
let recorder = new Recorder({
  sampleBits: 16, // 采样位数
  sampleRate: 16000, // 采样率
  numChannels: 1,
});
export default {
  data() {
    return {
      messages: [{ user: 1, content: "Hello，我是智能问答机器人~" }],
      input: "",
      senderId:
        new Date().toISOString() +
        Math.random().toString(36).substr(2).toUpperCase(),
      showTips: false,
      pending: false,
      recorder: null,
      pcmBlob: null,

      //波浪图-录音
      drawRecordId: null,
      oCanvas: null,
      ctx: null,
      //波浪图-播放
      drawPlayId: null,
      pCanvas: null,
      pCtx: null,
    };
  },
  mounted() {
    this.startCanvas();
  },
  components: {},
  methods: {
    downloadPcm() {
      recorder.downloadWAV();
    },
    recognize() {
      if (!recorder) return;
      else {
        this.pcmBlob = recorder.getPCMBlob();
        var time = recorder.duration;
        var size = recorder.fileSize;
        sendAudio(time, size, this.pcmBlob)
          .then((res) => {
            if (!res.data.code) {
              console.log(res.data.results);
              this.input += res.data.results;
            } else {
              // todo 错误识别处理
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
    startCanvas() {
      //录音波浪
      this.oCanvas = document.getElementById("canvas");
      this.ctx = this.oCanvas.getContext("2d");
      //播放波浪
      this.pCanvas = document.getElementById("canvas");
      this.pCtx = this.pCanvas.getContext("2d");
    },
    // 开始录音
    startRecorder() {
      if (!recorder)
        recorder = new Recorder({
          sampleBits: 16,
          sampleRate: 16000,
          numChannels: 1,
        });
      recorder.start().then(
        () => {
          this.drawRecord(); //开始绘制图片
        },
        (error) => {
          // 出错了
          console.log(`${error.name} : ${error.message}`);
        }
      );
    },
    // 结束录音
    stopRecorder() {
      recorder.stop();
      this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
      this.drawRecordId = null;
    },
    // 录音播放
    playRecorder() {
      recorder.play();
      this.drawPlay(); //绘制波浪图
    },
    // 销毁录音
    destroyRecorder() {
      recorder.destroy().then(function () {
        recorder = null;
        this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
        this.drawRecordId = null;
      });
    },
    getPermission() {
      Recorder.getPermission().then(
        () => {
          this.$Message.success("获取权限成功");
        },
        (error) => {
          console.log(`${error.name} : ${error.message}`);
        }
      );
    },

    /**
     * 绘制波浪图-录音
     * */
    drawRecord() {
      // 用requestAnimationFrame稳定60fps绘制
      this.drawRecordId = requestAnimationFrame(this.drawRecord);

      // 实时获取音频大小数据
      let dataArray = recorder.getRecordAnalyseData(),
        bufferLength = dataArray.length;

      // 填充背景色
      this.ctx.fillStyle = "rgb(200, 200, 200)";
      this.ctx.fillRect(0, 0, this.oCanvas.width, this.oCanvas.height);

      // 设定波形绘制颜色
      this.ctx.lineWidth = 2;
      this.ctx.strokeStyle = "rgb(0, 0, 0)";

      this.ctx.beginPath();

      var sliceWidth = (this.oCanvas.width * 1.0) / bufferLength, // 一个点占多少位置，共有bufferLength个点要绘制
        x = 0; // 绘制点的x轴位置

      for (var i = 0; i < bufferLength; i++) {
        var v = dataArray[i] / 128.0;
        var y = (v * this.oCanvas.height) / 2;

        if (i === 0) {
          // 第一个点
          this.ctx.moveTo(x, y);
        } else {
          // 剩余的点
          this.ctx.lineTo(x, y);
        }
        // 依次平移，绘制所有点
        x += sliceWidth;
      }

      this.ctx.lineTo(this.oCanvas.width, this.oCanvas.height / 2);
      this.ctx.stroke();
    },
    /**
     * 绘制波浪图-播放
     * */
    drawPlay() {
      // 用requestAnimationFrame稳定60fps绘制
      this.drawPlayId = requestAnimationFrame(this.drawPlay);

      // 实时获取音频大小数据
      let dataArray = recorder.getPlayAnalyseData(),
        bufferLength = dataArray.length;

      // 填充背景色
      this.pCtx.fillStyle = "rgb(200, 200, 200)";
      this.pCtx.fillRect(0, 0, this.pCanvas.width, this.pCanvas.height);

      // 设定波形绘制颜色
      this.pCtx.lineWidth = 2;
      this.pCtx.strokeStyle = "rgb(0, 0, 0)";

      this.pCtx.beginPath();

      var sliceWidth = (this.pCanvas.width * 1.0) / bufferLength, // 一个点占多少位置，共有bufferLength个点要绘制
        x = 0; // 绘制点的x轴位置

      for (var i = 0; i < bufferLength; i++) {
        var v = dataArray[i] / 128.0;
        var y = (v * this.pCanvas.height) / 2;

        if (i === 0) {
          // 第一个点
          this.pCtx.moveTo(x, y);
        } else {
          // 剩余的点
          this.pCtx.lineTo(x, y);
        }
        // 依次平移，绘制所有点
        x += sliceWidth;
      }

      this.pCtx.lineTo(this.pCanvas.width, this.pCanvas.height / 2);
      this.pCtx.stroke();
    },
    sendMessage(msg) {
      this.input = "";
      if (!msg) {
        return;
      }
      this.pending = true;
      this.messages.push({
        user: 0,
        content: msg,
      });
      sendMessage(this.senderId, msg)
        .then((res) => {
          if (!res.data.code) {
            console.log(res.data.results);
            this.messages.push({
              user: 1,
              content: res.data.results,
            });
            this.pending = false;
          } else {
            console.log(res.data.results);
            this.messages.push({
              user: 1,
              content: "你的问题我暂时理解不了哦...",
            });
            this.pending = false;
          }
        })
        .catch(() => {
          this.messages.push({
            user: 1,
            content: "发生了一些未知错误，稍后再试哦...",
          });
          this.pending = false;
        });
    },
    getMsg(msg) {
      if (Array.isArray(msg)) {
        return msg[Math.floor(Math.random() * msg.length)];
      }
      return msg;
    },
  },
};
</script>

<style lang="scss" scoped>
.qapage {
  height: 650px;
  position: relative;
  display: flex;
  flex-direction: column;
  background-color: rgb(245, 245, 245);
}
.canvas {
  position: relative;
  text-align: center;
}
.messages {
  overflow: scroll;
  height: 450px;
  margin-bottom: 20px;
  flex: 1;
  .chatbox {
    &.user0 {
      float: right;
      margin-right: 10px;
      background-color: rgb(158, 234, 106);
    }
    &.user1 {
      float: left;
      margin-left: 10px;
      background-color: white;
    }
    padding: 8px 18px 10px;
    max-width: 300px;
    border-radius: 6px;
    clear: both;
    color: black;
    font-size: 16px;
    margin: 5px 0;
  }
}
</style>
