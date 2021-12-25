# qa

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

└── qa                      #前端目录结构
  └── front-end
    ├── .gitignore
    ├── babel.config.js
    ├── LICENSE
    ├── package-lock.json
    ├── package.json
    ├── public
    │  └── index.html
    ├── README.md
    ├── src
    │  ├── api
    │  │  └── index.js          #定义的后端接口
    │  ├── App.vue              #系统主页
    │  ├── assets               #静态图片目录
    │  │  ├── home.png
    │  │  ├── logo.png
    │  │  ├── 各问答系统对比.png
    │  │  └── 后端流程展示.png
    │  ├── components
    │  ├── config.json
    │  ├── element-variables.scss
    │  ├── live2d.d.ts                #声明看板娘插件
    │  ├── main.js
    │  ├── plugins
    │  │  ├── element.js
    │  │  └── scroll.js
    │  ├── router
    │  │  └── index.js                #页面路由
    │  ├── store.js                   #存储
    │  └── views
    │    ├── Home.vue                 #概览页
    │    └── Qas.vue                  #问答页
    ├── structure.txt
    └── yarn.lock
