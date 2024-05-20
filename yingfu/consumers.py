import json

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.layers import get_channel_layer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    消费者---处理websocket连接 处理客户端发过来的消息
            使用channel_layer 进行连接分组 ，消息分发
    """

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        print("连接的房间名和channel_name", self.channel_name, self.room_group_name)
        await self.channel_layer.group_add(  # channel_layer.group_add() 这个是将websocket的连接加入到指定的组
            self.room_group_name,  # 根据room_group_name
            self.channel_name  # 每一个连接成功的都会有一个channel_name

            # 如果settings中是以redis作为存储room_group_name和channel_name的话
            # 就会以room_group_name为键 channel_name为值的方式进行存储
            # 后面进行消息分发时候通过键（群名）定位到聊天的客户端连接的channel_name
        )

        # 接受连接
        await self.accept()

        # 连接成功默认收到的提示语
        msg = {"content": "👏👏：您来了，随便聊聊", "level": 2}
        await self.send(text_data=json.dumps({
            'message': msg["content"]
        }))

        print(f'Client connected to room: {self.room_group_name}')

    # 每一个断开的链接都会触发disconnect方法
    async def disconnect(self, close_code):
        print("断开的房间名：", self.room_group_name)
        print("channel_name：", self.channel_name)

        await self.channel_layer.group_discard(  # group_discard() 将当前的websocket连接从组中移除
            self.room_group_name,
            self.channel_name
        )
        print(f'Client disconnected from room: {self.room_group_name}')

    # 接受到各个客户端的消息 进行消息转发
    async def receive(self, text_data=None, bytes_data=None):  # 接收消息时触发
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            # print(type(self.room_name))
            print("收到来自" + self.room_group_name + "房间的消息：", message)

            # 信息群发 ---- 根据之前group_add() 保存的客户端连接成功信息进行消息转发
            await self.channel_layer.group_send(  # group_send()  将消息发送给组中
                self.room_group_name,
                {"type": "chat_message",
                 "message": message}
            )

    # 自定义方法 将组中获取到的消息 传递给客户端  与上面方法receive 中type chat_message 对应
    # 没有实现这个方法的话 组中的消息将无法传递给客户端
    async def chat_message(self, event):  # event 从组中接受到消息/事件
        message = event['message']

        await self.send(text_data=json.dumps({
            "message": message
        }))
