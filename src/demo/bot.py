#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================================
#
# Copyright (c) 2019 Chatopera Inc. <https://chatopera.com> All Rights Reserved
#
#
# File: /Users/hain/chatopera/py-clause/clause/tst-demo.py
# Author: Hai Liang Wang
# Date: 2019-09-11:22:09:30
#
# ===============================================================================

"""
Clause Client   
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2019 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2019-09-11:22:09:30"

import os
import sys

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curdir, ".."))

if sys.version_info[0] < 3:
    # raise "Must be using Python 3"
    pass
else:
    unicode = str

# Get ENV
ENVIRON = os.environ.copy()

import pprint
log = pprint.PrettyPrinter(indent=4).pprint

from time import sleep

from clause import Client, Data
from clause import CustomDict, SysDict, DictWord
from clause import Intent, IntentSlot, IntentUtter
from clause import Entity, ChatMessage, ChatSession

## Other contants
chatbot_id = "avtr003"
intent_name = "takeOut"
customDictName= "food"

bot = Client(ENVIRON["CL_HOST"] if "CL_HOST" in ENVIRON else "localhost" , 
             ENVIRON["CL_PORT"] if "CL_PORT" in ENVIRON else 8056)

'''
自定义词典
'''
# 创建自定义词典
data = Data()
data.customdict = CustomDict(name=customDictName, 
                                chatbotID=chatbot_id)
resp = bot.postCustomDict(data)
# print("postCustomDict response: %s" % resp)

# 更新自定义词典
data = Data()
data.chatbotID = chatbot_id
data.customdict = CustomDict(name=customDictName, chatbotID=chatbot_id)
data.dictword = DictWord(word="西红柿", synonyms="狼桃;柿子;番茄")
resp = bot.putDictWord(data)
# print("putDictWord response: %s" % resp)

# 引用系统词典
data = Data()
data.chatbotID = chatbot_id
data.sysdict = SysDict(name="@TIME")
resp = bot.refSysDict(data)
print("refSysDict response: %s" % resp)

'''
意图管理
'''
# 创建意图
data = Data()
data.intent = Intent(chatbotID=chatbot_id, name=intent_name)
resp = bot.postIntent(data)
#print("postIntent response: %s" % resp)

# 创建意图槽位: 配菜
data = Data()
data.intent = Intent(chatbotID=chatbot_id, name=intent_name)
data.slot = IntentSlot(name="vegetable", requires=True, question="您需要什么配菜")
data.customdict = CustomDict(chatbotID=chatbot_id, name=customDictName)
resp = bot.postSlot(data)
#print("postSlot response: %s" % resp)

# 创建意图槽位: 送达时间
data = Data()
data.intent = Intent(chatbotID=chatbot_id, name=intent_name)
data.slot = IntentSlot(name="date", requires=True, question="您希望什么时候用餐")
data.sysdict = SysDict(name="@TIME")
resp = bot.postSlot(data)
#print("postSlot response: %s" % resp)

# 创建意图槽位: 送达位置
data = Data()
data.intent = Intent(chatbotID=chatbot_id, name=intent_name)
data.slot = IntentSlot(name="location", requires=True, question="外卖送到哪里")
resp = bot.postSlot(data)
#print("postSlot response: %s" % resp)

# 添加意图说法
data = Data()
data.intent = Intent(chatbotID=chatbot_id, name=intent_name)
data.utter = IntentUtter(utterance="帮我来一份{vegetable}，送到{location}")
resp = bot.postUtter(data)
data.utter = IntentUtter(utterance="我想点外卖")
resp = bot.postUtter(data)
# print("postUtter response: %s" % resp)

'''
训练机器人
'''
data = Data()
data.chatbotID = chatbot_id
resp = bot.train(data)
#print("train response: %s" % resp)

## 训练是一个长时间任务，进行异步反馈
while True:
    sleep(3)
    data = Data()
    data.chatbotID = chatbot_id
    resp = bot.status(data)
    if resp.rc == 0:
        break

'''
对话
'''
# 创建session
## 关于session的说明，参考 https://dwz.cn/wRFrELrq
data = Data()
data.session = ChatSession(chatbotID=chatbot_id,
   uid="py", # 用户唯一的标识
   channel="testclient", # 自定义，代表该用户渠道由字母组成
   branch="dev" # 测试分支，有连个选项：dev, 测试分支；pro，生产分支
   )
sessionId = bot.putSession(data).session.id
#print("putSession response: %s" % resp)

# 对话
data = Data()
data.session = ChatSession(id=sessionId)
text = "我想点外卖，来一份番茄"
log("chat human: %s" % text)
data.message = ChatMessage(textMessage=text)
resp = bot.chat(data)
log("chat bot: %s \n 意图: %s" % (resp.message.textMessage, resp.session))

text = "我想在下午三点用餐"
log("chat human: %s" % text)
data.message = ChatMessage(textMessage=text)
resp = bot.chat(data)
log("chat bot: %s \n 意图: %s" % (resp.message.textMessage, resp.session))

bot.destroy()