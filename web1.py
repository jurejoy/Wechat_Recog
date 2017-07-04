# -*- coding: utf-8 -*-

'''

【功能】
1.响应微信发送的Token验证
2.接收用户文本信息

【更新日期】2016.03.17
'''



import os
import web              #web.py
import time
import datetime
import hashlib          #hash加密算法
from lxml import etree  #xml解析
import requests         #http请求
import json
import codecs
from imgtest2 import *


#===================微信公众账号信息================================
#把微信开发页面中的相关信息填进来，字符串格式
my_appid = '******************'
my_secret = '*****************************'
#========匹配URL的正则表达式,url/将被WeixinInterface类处理===========
urls = ( '/','WeixinInterface' )

#===================微信权限交互====================================
def _check_hash(data):
    '''
    响应微信发送的GET请求(Hash校验)
    :param data: 接收到的数据
    :return: True or False，是否通过验证
    '''
    signature=data.signature  #加密签名
    timestamp=data.timestamp  #时间戳
    nonce=data.nonce          #随机数
    #自己的token
    token="wechat"   #这里改写你在微信公众平台里输入的token
    #字典序排序
    list=[token,timestamp,nonce]
    list.sort()   #拼接成一个字符串进行sha1加密,加密后与signature进行对比
    sha1=hashlib.sha1()
    map(sha1.update,list)
    hashcode=sha1.hexdigest() #sha1加密算法
    #如果是来自微信的请求，则回复echostr
    if hashcode == signature:
        return True
    return False

#=====================微信+HTTP server===============================
class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def _reply_text(self, toUser, fromUser, msg):
        '''
        回复文本消息
        :param fromUser:
        :param toUser:
        :param msg:要发送到的消息，文本格式
        :return:
        '''
        return self.render.reply_text(toUser, fromUser, int(time.time()),msg + '\n\ntime: ' + now_time)#加入时间戳

    def _recv_text(self, fromUser, toUser, xml):
        '''
        接收到文本消息，自动回复
        :param fromUser:
        :param toUser:
        :param xml:收到的xml文件
        :return:
        '''
        #提取xml中Content文本信息
        content = xml.find('Content').text
        reply_msg = content
        return self._reply_text(fromUser, toUser, u'你刚才说的是：' + reply_msg )

    def GET(self): #get,从指定的资源请求数据
        #获取输入参数
        data = web.input()
        if _check_hash(data):
            return data.echostr #微信发来的随机字符串,若验证通过,则返回echostr

    def POST(self): #post,向指定的资源提交数据
        '''
        ###########General POST#################
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        msgType=xml.find("MsgType").text #消息类型,包括text/event/image/voice/location/link等
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        #对不同类型的消息分别处理:
        if msgType == 'text':
            return self._recv_text(fromUser, toUser, xml)
        
        ############Repeat Contents################
        str_xml = web.data() #获得post来的数据 
        xml = etree.fromstring(str_xml)#进行XML解析 
        msgType=xml.find("MsgType").text 
        fromUser=xml.find("FromUserName").text 
        toUser=xml.find("ToUserName").text 
        if msgType == 'text':
            content=xml.find("Content").text
            return self.render.reply_text(fromUser,toUser,int(time.time()), content)
        elif msgType == 'image':
            pass
        else:
            pass
        '''
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        #content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType == 'image':
            picurl = xml.find("PicUrl").text
            print(picurl)
            mood = imgtest2(picurl)
            return self.render.reply_text(fromUser,toUser,int(time.time()), '亲，你的心情看起来似乎'+ mood)
        else:
            content = xml.find("Content").text  # 获得用户所输入的内容
            return self.render.reply_text(fromUser,toUser,int(time.time()), content)
            
'''
            try:
                content = xml.find("Content").text
                datas = imgtest(content)
                return self.render.reply_text(fromUser, toUser, int(time.time()), '图中人物性别为'+datas[0]+'\n'+'年龄为'+datas[1])
            except:
                return self.render.reply_text(fromUser, toUser, int(time.time()),  '识别失败，换张图片试试吧')
        else:
            content = xml.find("Content").text  # 获得用户所输入的内容
            return self.render.reply_text(fromUser,toUser,int(time.time()), content)
'''
#=====================启动app========================================

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()