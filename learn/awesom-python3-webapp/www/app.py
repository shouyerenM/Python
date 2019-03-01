#!/usr/bin/env python3
#!coding=utf-8

#需要的库，第三方库是aiohttp，jinja2，aiomysql
import logging; logging.basicConfig(level = logging.INFO)
#logging：系统日志，

import asyncio, os, json, time
#asyncio：异步IO，os：系统接口，json：json编码解码模块，time：系统时间模块
from datetime import datetime
#datetime：日期模块

from aiohttp import web
#siohttp：异步web开发框架

#WSGI接口，用于响应HTTP请求
#用于处理URL，将与具体url绑定
def index(request):
    return web.Response(body = b'<h1>Awesome<h1>',content_type='text/html')
    #通过response发送HTTP的header，返回body
    #参数：包含了浏览器发送过来的HTTP协议里的信息，一般不用自己构造。
    #返回值：web.response（body=“...”）构造。

#启用WSGI服务器，用于加载index
@asyncio.coroutine
#创建协程
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    #创建web服务器，并将index函数注册进其函数其应用路径（Application.router）
    #创建web服务器实例app，也就是aiohttp.web.Application类的实例，作用是处理url和http协议
    #将index函数注册进app.router中
    srv =yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
    #异步调用yield from后的命令，转到event loop里
    #用协程监听服务，并使用aiohttp中的HTTP协议簇
    #其中loop为传入函数的协程，调用其类方法创建一个监听服务
    #yield from返回一个创建好的，绑定ip，端口，HTTP协议簇的监听服务的协程。
    #yield from的作用是使srv的行为模式和loop.create_server()一致
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
#从yield from处获取event loop（事件循环），启动新线程进行IO操作
loop.run_until_complete(init(loop))
#执行带有协程的函数
loop.run_forever()
