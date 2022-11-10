"""
ASGI config for test_task project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from stories import consumers

from django.urls import re_path,path
from django.core.asgi import get_asgi_application
import stories.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_task.settings')







application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
URLRouter(
[path('test_task/notification_testing/',consumers.NotificationConsumer.as_asgi())]
))
        
})
