import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stock_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stock_updates", self.channel_name)

    async def receive(self, text_data):
        # We don’t expect clients to send data, so this is empty for now
        pass

    async def send_stock_update(self, event):
        print(f"Received stock update: {event['data']}") # debug
        stock_data = event['data']
        await self.send(text_data=json.dumps(stock_data))
