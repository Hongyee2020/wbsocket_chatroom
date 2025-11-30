"""  这个 asgi.py 是你的 Django 项目的 “总网关”，它能让你的网站同时支持：

🌐 普通网页访问（HTTP）
🔁 实时通信功能（WebSocket） """

import os                                                                 
# 导入操作系统模块，用于设置环境变量（如指定Django配置文件）

from channels.auth import AuthMiddlewareStack                           
# 导入Channels的认证中间件栈，用于在WebSocket连接中识别用户登录状态（类似request.user）
from channels.routing import ProtocolTypeRouter, URLRouter             
 # 导入协议路由工具：ProtocolTypeRouter根据协议类型分发请求，URLRouter实现WebSocket的URL路由
from django.core.asgi import get_asgi_application                      
# 获取Django默认的ASGI应用实例，用来处理HTTP请求（普通网页访问）
import chat.routing                                                  
 # 导入自定义的WebSocket路由模块（定义了WebSocket的URL路径规则，比如/ws/chat/）

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')    
# 设置环境变量：告诉Django使用哪个settings文件（这里用的是mysite/settings.py）

django_asgi_app = get_asgi_application()                              
# 创建一个标准的Django ASGI应用，用于处理所有HTTP请求（如加载网页、表单提交等）

application = ProtocolTypeRouter({                                     
    # 定义主ASGI应用入口，根据请求的协议类型进行分发
    "http": django_asgi_app,                                           
    # 如果是HTTP请求（例如浏览器打开网页），交给Django默认应用处理
    "websocket": AuthMiddlewareStack(                                  
        # 如果是WebSocket请求（实时通信），先经过认证中间件（带上用户信息）
        URLRouter(chat.routing.websocket_urlpatterns)                  
        # 再通过URL路由器，将不同WebSocket路径分发给对应的Consumer处理（如聊天功能）
    ),                                                                  
    # 例如：ws://127.0.0.1:8000/ws/chat/room1/ → 被路由到特定consumer
})                                                                     
 # 结束ProtocolTypeRouter配置
