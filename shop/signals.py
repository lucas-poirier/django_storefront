from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Product
import logging

@receiver(post_save, sender=Product)
def broadcast_stock_update(sender, instance, **kwargs):
    print(f"Signal triggered: {instance.name} - {instance.stock}") # debug
    channel_layer = get_channel_layer()
    data = {
        'id': instance.id,
        'name': instance.name,
        'stock': instance.stock,
    }

    # logger.info(f"Broadcasting stock update: {data}")  # Check if this appears in logs
    
    async_to_sync(channel_layer.group_send)(
        "stock_updates",
        {
            "type": "send_stock_update",
            "data": data,
        }
    )
    # Notify all connected WebSocket clients about the stock update
    # This will be handled in the StockConsumer