# BIT_QA_System

## 后端

### 运行方法

后端语言为Python，要运行服务器，请执行：

```shell
cd QA/backend/
python3 server.py
```

也可在本地使用命令行直接启动问答：

```shell
cd QA/backend/
python3 interactive_qa.py
```

### 所需运行环境

python>=3.8

pytorch==1.9.1

transformers==4.12.5

scipy==1.6.2

flask==1.1.2

flask_cors==3.0.10

OpenCC

numpy

scikit-learn

colorama

### 代码结构

```
QA
└─backend
    │  .gitignore
    │  interactive_qa.py  在本地命令行与问答系统交互的脚本
    │  qa.py  问答系统类，提供接受问题返回回答的接口
    │  reader.py  阅读器类，封装模型
    │  server.py  运行服务器的脚本
    │  test_hash.py  工具用脚本，检查是不是有n-gram哈希冲突
    │
    └─retriever
        │  .gitignore
        │  data_paths.py  生成数据文件的路径，供各个地方使用
        │  doc_db.py  封装了文档数据库的简单SQL操作
        │  mytokenizer.py  提供分词和生成n-gram特征的接口
        │  ranker.py  检索器类，提供检索文档并排序的接口
        │  README.md  检索器部分的详细介绍可查看此文件
        │  run_build_doc_db.py  读取数据并构建文档数据库的脚本
        │  run_build_tf-idf.py  读取数据库并构建TF-IDF矩阵的脚本
        │  stopwords.json
        │  utils.py
        │  __init__.py
        │
        └─customize
                out(1).json  我们构建的北理工领域的文档集
```

## 前端

### Project setup
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


