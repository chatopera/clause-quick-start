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

```
git clone https://github.com/chatopera/clause-py-demo.git
```

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

> 注意：clause 服务会在成功启动前，重启若干次，因为它需要检查 MySQL 的初始化状态，MySQL 第一次启动因为需要初始化，所以需要 20-30 秒！

## 执行示例程序

```
cd clause-py-demo
./scripts/demo.sh
```

该脚本执行的示例代码[bot.py](https://github.com/chatopera/clause-py-demo/blob/master/src/demo/bot.py)内有注释介绍如何完成：

| 步骤 | 说明           |
| ---- | -------------- |
| 1    | 创建自定义词典 |
| 2    | 添加自定义词条 |
| 3    | 引用系统词典   |
| 4    | 创建意图       |
| 5    | 添加意图槽位   |
| 6    | 添加意图说法   |
| 7    | 训练机器人     |
| 8    | 创建会话       |
| 9    | 和机器人对话   |

示例程序是一个点餐程序，输出内容如下：

```
'chat human: 我想点外卖，来一份番茄'
('chat bot: 您希望什么时候用餐 \n'
 " 意图: ChatSession(intent_name='takeOut', chatbotID='avtr003', uid='py', "
 "channel='testclient', resolved=False, id='8314A948BBB4CFD8FB92D2E800000000', "
 "entities=[Entity(name='vegetable', val='番茄', requires=True, "
 "dictname='food'), Entity(name='date', val='', requires=True, "
 "dictname='@TIME')], branch='dev', createdate='2019-09-27 10:41:01', "
 "updatedate='2019-09-27 10:41:01')")
'chat human: 我想在下午三点用餐'
('chat bot: None \n'
 " 意图: ChatSession(intent_name='takeOut', chatbotID='avtr003', uid='py', "
 "channel='testclient', resolved=True, id='8314A948BBB4CFD8FB92D2E800000000', "
 "entities=[Entity(name='vegetable', val='番茄', requires=True, "
 "dictname='food'), Entity(name='date', val='下午三点', requires=True, "
 "dictname='@TIME')], branch='dev', createdate='2019-09-27 10:41:01', "
 "updatedate='2019-09-27 10:41:01')")
(venv-py3)
```

详细了解程序，[参考文档](https://github.com/chatopera/clause/wiki/%E7%A4%BA%E4%BE%8B%E7%A8%8B%E5%BA%8F)。

## 停止服务并清空数据

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
