# 从 Django 的 URL 系统导入 re_path，支持使用正则表达式匹配请求路径（比普通 path 更灵活，适合 WebSocket 动态路由）
from django.urls import re_path

# 导入当前应用目录下的 consumers 模块，其中定义了处理 WebSocket 连接的消费者类（如接收消息、广播数据等）
from . import consumers

# 定义 WebSocket 路由列表，ASGI 应用会根据此列表判断哪些路径启用实时通信功能
websocket_urlpatterns = [

    # 匹配以 ws://<host>/ws/chat/ 结尾的 WebSocket 连接请求
    # 并将其交由 ChatConsumer 的 ASGI 实例处理（.as_asgi() 是标准调用方式）
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]
