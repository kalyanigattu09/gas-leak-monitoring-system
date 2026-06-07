import json

from channels.generic.websocket import AsyncWebsocketConsumer


class GasMonitoringConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('gas_monitoring', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('gas_monitoring', self.channel_name)

    async def gas_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'gas_update',
            'reading': event.get('reading'),
            'alert': event.get('alert'),
        }))
