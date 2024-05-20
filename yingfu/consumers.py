import json

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.layers import get_channel_layer
import aioredis

"""
书写消费者连接，收到消息的功能
"""

# 定义 Redis 客户端，连接到本地 Redis 服务
redis = aioredis.from_url('redis://localhost:6379', encoding="utf-8", decode_responses=True)


# 定义 ChatConsumer 类，继承自 AsyncWebsocketConsumer 类
class ChatConsumer(WebsocketConsumer):

    # async def connect(self):
    #     #     # 建立 WebSocket 连接
    #     #     await self.accept()
    #     #
    #     #     # 获取用户信息（这里简化为从 scope 中获取用户名）
    #     #     user = self.scope['user']
    #     #
    #     #     # 获取房间信息（这里简化为从 URL 参数中获取房间名）
    #     #     room_name = self.scope['url_route']['kwargs']['room_name']
    #     #
    #     #     message = {"type": "connect",
    #     #                "user": user.username,
    #     #                "room": room_name}
    #     #
    #     #     # 发送连接成功消息给客户端，包含用户信息和房间信息
    #     #     await self.send(text_data=json.dumps(message))

    def websocket_connect(self, message):
        # 有客户端向后端发送 WebSocket 连接的请求时，自动触发(握手)
        self.accept()
        print("连接成功")
        # 获取房间号
        group_num = self.scope["url_route"]['kwargs']['room_name']

        print(group_num)

    def websocket_receive(self, message):
        # 浏览器基于 WebSocket 向后端发送数据，自动触发接收消息
        print(message)
        self.send("不要回复不要回复！！！")

    def websocket_disconnect(self, message):
        # 客户端向服务端断开连接时，自动触发
        print("对方连接断开！！")
        raise StopConsumer()


