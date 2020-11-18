"""
ASGI config for question_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.urls import re_path
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from . import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'question_project.settings')

websocket_urlpatterns = [
    re_path(r'ws/quiz/(?P<quiz_id>.+)$', consumers.QuizConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
