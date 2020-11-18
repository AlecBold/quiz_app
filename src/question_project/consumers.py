from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


from .models import UserModel, Quiz, Question


class QuizConsumer(WebsocketConsumer):

    def connect(self):
        pass

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        pass
