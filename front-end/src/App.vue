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

    <el-container>
      <live2d
        ref="aaa"
        style="z-index: 10"
      ></live2d>
      <el-main>
        <!-- <el-drawer :visible.sync="drawer" direction="ltr" :show-close="false">
      <el-menu router @select="drawer = false">
        <el-menu-item index="/"> Home </el-menu-item>
        <el-menu-item index="/docs"> Documents </el-menu-item>
      </el-menu>
    </el-drawer> -->

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
  components: {}
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
  font-size: 14px;
}

.head {
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
