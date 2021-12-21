<template>
  <el-container>
    <el-header>
      <el-card>
        <span class="title">📣QA System</span>

        <el-tag>
          <router-link to="/Qas">问答(Qustions) | </router-link>
          <router-link to="/">功能(Functions)</router-link>
        </el-tag>
      </el-card>
    </el-header>

    <el-container>
      <live2d
        @live2dItemClick="live2dItemClick"
        @live2dItemEnter="live2dItemEnter"
        ref="aaa"
        :className="className"
      ></live2d>
      <el-main>
        <!-- <el-drawer :visible.sync="drawer" direction="ltr" :show-close="false">
      <el-menu router @select="drawer = false">
        <el-menu-item index="/"> Home </el-menu-item>
        <el-menu-item index="/docs"> Documents </el-menu-item>
      </el-menu>
    </el-drawer> -->

        <transition name="fade-transform" mode="out-in">
          <router-view />
        </transition>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: "app",
  components: {},
  mounted() {
    setTimeout(() => {
      window.L2Dwidget.init({
        pluginRootPath: "../public/live2dw/",
        pluginJsPath: "lib/",
        pluginModelPath: "live2d-widget-model-z16/assets/",
        tagMode: false,
        debug: false,
        model: {
          jsonPath: "../live2dw/live2d-widget-model-z16/assets/z16.model.json",
        },
        display: { position: "left", width: 100, height: 200 },
        mobile: { show: true },
        log: false,
      });
    }, 1000);
  },
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
  width: 800px;
  position: relative;
  margin: 0 auto;
  flex-direction: column;
}

.el-tag {
  position: relative;
  margin-left: 20px;
}

.el-card {
  margin: 0 auto;
  position: relative;
}
.container {
  margin: 40px auto;
  width: 800px;
  height: 600px;
  position: relative;
  display: flex;
  flex-direction: column;
}
</style>
