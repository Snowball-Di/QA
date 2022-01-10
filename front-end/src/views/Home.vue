<template>
  <el-carousel height="800px" interval="5000" indicator-position="outside">
    <el-carousel-item>
      <el-card class="displayinfo">
        <span>本系统作者：habareraa, Snowball, Carl-Carl, CZY。 </span>
        <br />
        <br />
        <span> 前端Vue，后端Python，接口形式url，通信格式json。 </span>
        <br />
        <br />
        <span>
          基于文本阅读的问答系统，北理工相关问题问答&开放领域问答...
        </span>
        <br />
        <br />
        <span>Github地址: https://github.com/Snowball-Di/QA </span>
        <div class="demo-image">
          <el-image
            style="width: 325px; height: 282px; margin: 20px"
            :src="home"
          ></el-image>
        </div>
      </el-card>
    </el-carousel-item>

    <el-carousel-item>
      <el-card class="displayinfo">
        问答系统实现方式对比
        <br />
        <br />
        <div class="demo-image">
          <el-image style="width: 600px; height: 350px" :src="cmp"></el-image>
        </div>
      </el-card>
    </el-carousel-item>

    <el-carousel-item>
      <el-card class="displayinfo">
        后端模型流程展示
        <br />
        <br />
        <div class="demo-image">
          <el-image
            style="width: 600px; height: 400px"
            :src="back"
          ></el-image></div
      ></el-card>
    </el-carousel-item>

    <el-carousel-item>
      <el-card class="displayinfo">
        基于Vue框架的前端开发
        <div class="demo-image">
          <el-image
            :src="logo"
            style="width: 400px; height: 400px"
          ></el-image></div
      ></el-card>
    </el-carousel-item>
  </el-carousel>
</template>

<style>
.displayinfo {
  text-align: center;
  height: 480px;
  width: auto;
  align-content: center;
  border: 2px black;
  z-index: 0;
}

.el-image {
  align-content: center;
}
</style>

<script>
export default {
  data() {
    return {
      back: require("../assets/后端流程展示.png"),
      cmp: require("../assets/各问答系统对比.png"),
      home: require("../assets/home.png"),
      logo: require("../assets/logo.png"),
    };
  },
};
</script>