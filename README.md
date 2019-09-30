[![Docker Layers](https://images.microbadger.com/badges/image/chatopera/clause:develop.svg)](https://microbadger.com/images/chatopera/clause:develop "Image layers") [![Docker Version](https://images.microbadger.com/badges/version/chatopera/clause:develop.svg)](https://microbadger.com/images/chatopera/clause:develop "Image version") [![Docker Pulls](https://img.shields.io/docker/pulls/chatopera/clause.svg)](https://hub.docker.com/r/chatopera/clause/) [![Docker Stars](https://img.shields.io/docker/stars/chatopera/clause.svg)](https://hub.docker.com/r/chatopera/clause/) [![Docker Commit](https://images.microbadger.com/badges/commit/chatopera/clause:develop.svg)](https://microbadger.com/images/chatopera/clause:develop "Image CommitID")

<p align="center">
  <b>Clause项目QQ交流群：809987971， <a href="https://jq.qq.com/?_wv=1027&k=5JpEvBZ" target="_blank">点击链接加入群聊</a></b><br>
  <img src="https://user-images.githubusercontent.com/3538629/64315364-6a095380-cfe4-11e9-8bf6-f15ce6e26e0a.png" width="200">
</p>

<p align="center">
  <a href="https://github.com/chatopera/clause" target="_blank">
      <img src="https://user-images.githubusercontent.com/3538629/64316956-e4d46d80-cfe8-11e9-8342-ec8a250074bf.png" width="800">
  </a>
</p>

# Clause Tutorials for Python

Chatopera Language Understanding Service，Chatopera 语义理解服务

Python 示例程序

![Sep-30-2019 23-14-13-min](https://user-images.githubusercontent.com/3538629/65892122-54ffc480-e3d8-11e9-8f64-c82f25694df5.gif)

## 前提

- Linux 操作系统
- 命令行终端，并且具有 sudo 权限
- 安装完毕 Docker、Docker Compose 和 Python3.x。

## 下载镜像

```
cd clause-py-demo
docker-compose pull
```

## 安装依赖

下载示例代码

```
git clone https://github.com/chatopera/clause-py-demo.git
```

安装 Clause Python Package

```
cd clause-py-demo
./scripts/install.sh
```

## 运行服务

```
cd clause-py-demo
./scripts/start.sh
```

上面命令会执行一段时间，并且输出日志，在控制台内，直到打印如下输出：

```
clause_1    | I0927 10:39:39.517269     1 main.cpp:80] serving on port 8056
clause_1    | Thrift: Fri Sep 27 10:39:39 2019 TNonblockingServer: Serving with 1 io threads.
clause_1    | Thrift: Fri Sep 27 10:39:39 2019 TNonblockingServer: using libevent 2.1.10-stable method epoll
clause_1    | Thrift: Fri Sep 27 10:39:39 2019 TNonblocking: IO thread #0 registered for listen.
clause_1    | Thrift: Fri Sep 27 10:39:39 2019 TNonblocking: IO thread #0 registered for notify.
clause_1    | Thrift: Fri Sep 27 10:39:39 2019 TNonblockingServer: IO thread #0 entering loop...
```

**代表服务成功启动！**

## 执行示例程序

```
cd clause-py-demo
./scripts/demo.sh
```

该脚本执行的示例代码[bot.py](https://github.com/chatopera/clause-py-demo/blob/master/src/demo/bot.py)内有注释介绍如何完成：

| 步骤 | 说明                   |
| ---- | ---------------------- |
| 1    | 清除该机器人之前的数据 |
| 2    | 创建自定义词典         |
| 3    | 添加自定义词条         |
| 4    | 创建意图               |
| 5    | 添加意图槽位           |
| 6    | 添加意图说法           |
| 7    | 训练机器人             |
| 8    | 创建会话               |
| 9    | 和机器人对话           |

示例程序是一个点餐程序，输出内容如下：

```
[connect] clause host 127.0.0.1, port 8056
[clean_up_bot] remove intent take_out
[clean_up_bot] remove customdict food
[create] dict name food
[create] intent name take_out
[create] intent slot time
[create] intent slot loc
[create] intent slot food
[create] intent utter 我想订一份{food}
[create] intent utter 我想点外卖
[create] intent utter 我想点一份外卖，{time}用餐
[create] intent utter 我想点一份{food}，送到{loc}
[train] start to train bot ...
[train] in progress ...
[chat] human: 我想点外卖，来一份汉堡包
[chat] bot: 您想什么时候送到？
[chat] human: 今天下午5点
[chat] bot: 您希望该订单送到哪里？
[chat] human: 送到大望路5号20楼
[chat] bot: 好的
[session] 订单信息： 收集信息已完毕 True
    intent: take_out
    entities:
        food: 汉堡包
        time: 今天下午5点
        loc: 大望路5号
```

详细了解程序，[参考文档](https://github.com/chatopera/clause/wiki/%E7%A4%BA%E4%BE%8B%E7%A8%8B%E5%BA%8F)。

## 输入文件

需要强调的是，该示例程序使用了 [profile.json](https://github.com/chatopera/clause-py-demo/blob/master/src/demo/profile.json) 文件作为机器人的输入数据，该文件描述了机器人的词典、说法和槽位等信息。

[profile.json](https://github.com/chatopera/clause-py-demo/blob/master/src/demo/profile.json) 内容如下：

```
{
  "chatbotID": "bot007",
  "dicts": [
    {
      "name": "food",
      "dictwords": [
        {
          "word": "汉堡",
          "synonyms": "汉堡包;漢堡;漢堡包"
        }
      ]
    }
  ],
  "intents": [
    {
      "name": "take_out",
      "description": "下外卖订单",
      "slots": [
        {
          "name": "time",
          "dictname": "@TIME",
          "requires": true,
          "question": "您想什么时候送到？"
        },
        {
          "name": "loc",
          "dictname": "@LOC",
          "requires": true,
          "question": "您希望该订单送到哪里？"
        },
        {
          "name": "food",
          "dictname": "food",
          "requires": true,
          "question": "您需要什么食物?"
        }
      ],
      "utters": [
        {
          "utterance": "我想订一份{food}"
        }
      ]
    }
  ]
}
```

开发者可以很方便的通过修改这个文件复用[bot.py](https://github.com/chatopera/clause-py-demo/blob/master/src/demo/bot.py)脚本训练和请求机器人对话服务。

## 停止服务并清空数据

恢复该示例项目到初始状态。

```
cd clause-py-demo
./scripts/flush.sh
```

## 获得技术支持

创建新的 Issue
https://github.com/chatopera/clause/issues

## 了解更多

Clause Wiki
https://github.com/chatopera/clause/wiki

## 开源许可协议

Copyright (2019) <a href="https://www.chatopera.com/" target="_blank">北京华夏春松科技有限公司</a>

[Apache License Version 2.0](https://github.com/chatopera/clause-py-demo/blob/master/LICENSE)

[![chatoper banner][co-banner-image]][co-url]

[co-banner-image]: https://user-images.githubusercontent.com/3538629/42383104-da925942-8168-11e8-8195-868d5fcec170.png
[co-url]: https://www.chatopera.com
