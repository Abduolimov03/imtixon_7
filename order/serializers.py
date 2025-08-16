from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    class Meta:
        model = OrderItem
        fields = ['id', 'card', 'product', 'amount', 'created_at', 'updated_at', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status' ,'created_at', 'updated_at',  'total_price', 'items']
