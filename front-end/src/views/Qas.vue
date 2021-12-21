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
  </el-card>
</template>

<script>
import { sendMessage } from "@/api";

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
    };
  },
  components: {},
  methods: {
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
              content: "你的问题我暂时理解不了哦 : )",
            });
          }
        })
        .catch(() => {
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
  height: 600px;
  position: relative;
  display: flex;
  flex-direction: column;
}

.messages {
  overflow: scroll;
  height: 500px;
  margin-bottom: 20px;
  flex: 1;
  .chatbox {
    &.user0 {
      float: right;
      margin-right: 10px;
    }
    &.user1 {
      float: left;
    }
    padding: 5px 15px 6px;
    max-width: 300px;
    border: 1px solid #2d8cf0;
    border-radius: 4px;
    clear: both;
    color: #2d8cf0;
    font-size: 13px;
    margin: 2px 0;
  }
}
</style>
