#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================================
#
# Copyright (c) 2019 Chatopera Inc. <https://www.chatopera.com> All Rights Reserved
#
#
# File: /Users/hain/chatopera/clause-py-demo/src/demo/bot.py
# Author: Hai Liang Wang
# Date: 2019-09-30:18:07:39
#
# ===============================================================================

from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2019 Chatopera Inc. All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2019-09-30:18:07:39"

import os
import sys

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    # raise "Must be using Python 3"
    pass
else:
    unicode = str

# Get ENV
ENVIRON = os.environ.copy()

import json
from time import sleep

from clause import Client, Data
from clause import CustomDict, SysDict, DictWord, DictPattern, DictPatternCheck
from clause import Intent, IntentSlot, IntentUtter
from clause import Entity, ChatMessage, ChatSession

CL_HOST = ENVIRON["CL_HOST"] if "CL_HOST" in ENVIRON else "127.0.0.1"
CL_PORT = ENVIRON["CL_PORT"] if "CL_PORT" in ENVIRON else 8056

def load_profile_json():
    '''
    加载Profile文件，Profile文件描述了该机器人的输入的训练数据
    '''
    with open(os.path.join(curdir, "profile.json"), 'r') as f:
        return json.load(f)


def check_profile(profile):
    '''
    校验Profile数据
    '''
    valid = True
    if profile is None: valid = False
    if not "chatbotID" in profile: valid = False
    if not "intents" in profile: valid = False

    # TODO 校验槽位中系统词典的名称
    # TODO 校验槽位中自定义词典的名称
    return valid

def clean_up_bot(bot, chatbotID):
    '''
    删除指定BOT的数据
    '''
    # 删除意图
    resp = bot.getIntents(Data(chatbotID=chatbotID,
                               pagesize=1000,
                               page=1))
    if resp.intents and len(resp.intents) > 0:
        for x in resp.intents:
            # 删除意图，该接口会删除关联的意图说法和槽位
            print("[clean_up_bot] remove intent %s" % x.name)
            bot.delIntent(Data(id=x.id))

    # 删除自定义词典
    resp = bot.getCustomDicts(Data(chatbotID=chatbotID,
                                   page=1,
                                   pagesize=1000))
    if resp.customdicts and len(resp.customdicts) > 0:
        for x in resp.customdicts:
            # 删除关联的词条和词典
            print("[clean_up_bot] remove customdict %s" % x.name)
            bot.delCustomDict(Data(chatbotID=chatbotID,
                                   customdict=CustomDict(chatbotID=chatbotID, name=x.name)))

    # 取消引用系统词典
    resp = bot.mySysdicts(Data(chatbotID=chatbotID))
    if resp.sysdicts and len(resp.sysdicts) > 0:
        for x in resp.sysdicts:
            print("[clean_up_bot] unref sysdict %s" % x.name)
            bot.unrefSysDict(Data(chatbotID=chatbotID, sysdict=SysDict(name=x.name)))


if __name__ == '__main__':
    profile = load_profile_json()
    if not check_profile(profile): raise Exception("Error in profile data.")

    chatbotID = profile["chatbotID"]

    '''
    录入BOT数据
    '''
    # create bot
    print("[connect] clause host %s, port %s" % (CL_HOST, CL_PORT))
    bot = Client(CL_HOST, CL_PORT)
    clean_up_bot(bot, chatbotID)

    # create customdict
    if "dicts" in profile:
        for x in profile["dicts"]:
            print("[create] dict name %s" % x["name"])
            bot.postCustomDict(Data(customdict=CustomDict(name=x["name"], chatbotID=chatbotID, type=x["type"])))

            # 词表词典
            if x["type"] == "vocab" and "dictwords" in x:
                [bot.putDictWord(Data(chatbotID=chatbotID,
                                      customdict=CustomDict(name=x["name"]),
                                      dictword=DictWord(word=y["word"],
                                                        synonyms=y["synonyms"] if "synonyms" in y else None))) for y in
                 x["dictwords"]]

            # 正则表达式词典
            if x["type"] == "regex" and "patterns" in x:
                bot.putDictPattern(Data(customdict = CustomDict(name=x["name"], 
                                            chatbotID=chatbotID),
                            dictpattern = DictPattern(patterns = x["patterns"])))

    # create intent
    for x in profile["intents"]:
        # 创建意图
        print("[create] intent name %s" % x["name"])
        bot.postIntent(Data(intent=Intent(name=x["name"], chatbotID=chatbotID)))
        if "description" in x and x["description"].rstrip(): bot.putIntent(
            Data(intent=Intent(chatbotID=chatbotID, name=x["name"], description=x["description"])))

        ## 创建槽位
        if "slots" in x:
            for y in x["slots"]:
                print("[create] intent slot %s" % y["name"])
                bot.postSlot(Data(intent=Intent(chatbotID=chatbotID, name=x["name"]),
                                  slot=IntentSlot(name=y["name"],
                                                  requires=y["requires"],
                                                  question=y["question"]),
                                  customdict=CustomDict(chatbotID=chatbotID, name=y["dictname"]) if not y[
                                      "dictname"].startswith("@") else None,
                                  sysdict=SysDict(name=y["dictname"]) if y["dictname"].startswith("@") else None))

        ## 创建说法
        if "utters" in x:
            for y in x["utters"]:
                print("[create] intent utter %s" % y["utterance"])
                bot.postUtter(Data(intent=Intent(chatbotID=chatbotID, name=x["name"]),
                                   utter=IntentUtter(utterance=y["utterance"])))

    '''
    训练机器人
    '''
    print("[train] start to train bot ...")
    resp = bot.train(Data(chatbotID=chatbotID))
    if resp.rc != 0:
        print("[train] error %s" % resp)
        raise Exception("Unexpected response with training bot request.")

    ## 训练是一个长时间任务，进行异步反馈
    while True:
        sleep(3)
        resp = bot.status(Data(chatbotID=chatbotID))
        print("[train] in progress ...")
        if resp.rc == 0:
            break

    '''
    对话
    '''
    # 创建session
    ## 关于session的说明，参考 https://dwz.cn/wRFrELrq
    session = bot.putSession(Data(session=ChatSession(chatbotID=chatbotID,
                                                      uid="py",  # 用户唯一的标识
                                                      channel="testclient",  # 自定义，代表该用户渠道由字母组成
                                                      branch="dev"  # 测试分支，有连个选项：dev, 测试分支；pro，生产分支
                                                      ))).session

    # 对话
    text = "我想点外卖，来一份汉堡包"
    print("[chat] human: %s" % text)
    ## 训练后，初次对话时会进行BOT的初始化，因此第一次回复会稍慢，大约2秒左右
    ## 完成初始化后的聊天请求才能代表系统正常的处理速度！
    resp = bot.chat(Data(session=ChatSession(id=session.id), message=ChatMessage(textMessage=text)))
    print("[chat] bot: %s" % (resp.message.textMessage))

    dummy_chat = lambda msg: "今天下午5点" if "时候" in msg else ( "送到大望路5号20楼" if "送到哪里" in msg else "我的联系方式15801818127" )

    text = dummy_chat(resp.message.textMessage)
    print("[chat] human: %s" % text)
    resp = bot.chat(Data(session=ChatSession(id=session.id), message=ChatMessage(textMessage=text)))
    print("[chat] bot: %s" % (resp.message.textMessage))

    text = dummy_chat(resp.message.textMessage)
    print("[chat] human: %s" % text)
    resp = bot.chat(Data(session=ChatSession(id=session.id), message=ChatMessage(textMessage=text)))
    print("[chat] bot: %s" % (resp.message.textMessage))
    
    text = dummy_chat(resp.message.textMessage)
    print("[chat] human: %s" % text)
    resp = bot.chat(Data(session=ChatSession(id=session.id), message=ChatMessage(textMessage=text)))
    # print("[chat] bot: %s" % (resp.message.textMessage))
    print("[chat] bot: %s" % ("好的" if resp.session.resolved else "[错误] 返回不符合逻辑"))

    ## 打印意图和槽位的信息
    print("[session] 订单信息： 收集信息已完毕 %s\n    intent: %s \n    entities:" % (resp.session.resolved, resp.session.intent_name))
    for x in resp.session.entities:
        print("        %s: %s" % (x.name, x.val))

    bot.destroy()
