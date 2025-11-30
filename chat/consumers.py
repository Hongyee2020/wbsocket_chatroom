# 导入 Python 标准库中的 json 模块，用于将 Python 字典转换为 JSON 字符串（前端 JavaScript 易于解析）
import json

# 从 Django Channels 中导入 AsyncWebsocketConsumer
# 这是一个支持异步操作的 WebSocket 消费者基类，适用于高并发实时通信场景（如传感器数据流）
from channels.generic.websocket import AsyncWebsocketConsumer


# 定义一个名为 ChatConsumer 的消费者类，继承自 AsyncWebsocketConsumer
# 它负责处理 WebSocket 连接的整个生命周期：连接建立、接收消息、断开连接等
class ChatConsumer(AsyncWebsocketConsumer):

    # 异步方法：当客户端发起 WebSocket 连接请求时自动调用
    async def connect(self):
        # 接受 WebSocket 连接（必须显式调用 accept()，否则连接会被拒绝）
        await self.accept()

        # 向客户端发送一条确认消息，表示连接已成功建立
        # 使用 json.dumps 将字典转换为 JSON 字符串，符合 WebSocket 消息格式标准
        await self.send(text_data=json.dumps({
            'message': '连接成功！'
        }))

    # 异步方法：当客户端通过 WebSocket 发送消息时自动调用
    # text_data: 接收到的文本消息（字符串格式），bytes_data: 二进制数据（本例未使用）
    async def receive(self, text_data=None, bytes_data=None):
        # 将接收到的消息原样返回给客户端，并添加前缀说明
        # 同样使用 JSON 格式封装响应内容
        await self.send(text_data=json.dumps({
            'message': f'你发送了: {text_data}'
        }))
