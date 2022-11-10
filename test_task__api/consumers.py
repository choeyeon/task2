from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync,sync_to_async
from channels.layers import get_channel_layer




@database_sync_to_async
def create_notification(receiver,typeof="task_created",status="unread"):
    notification_to_create=notifications.objects.create(user_revoker=receiver,type_of_notification=typeof)
    print('I am here to help')
    return (notification_to_create.user_revoker.username,notification_to_create.type_of_notification)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self,event):
        print('connected',event)
        print('Am i finallyy here')
        print(self.scope['user'].id)
        await self.accept()
        await self.send(json.dumps({
            "type":"websocket.send",
            "text":"hello world"
            }))

        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        self.send({
                "type":"websocket.send",
                "text":"room made"
                })
        
    async def send_notification(self,event):
        await self.send(json.dumps({
            "type":"websocket.send",
            "data":event
        }))
        print('I am here')
        print(event)
