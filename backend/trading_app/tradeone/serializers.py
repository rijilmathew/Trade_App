# trading/serializers.py
from rest_framework import serializers
from .models import Stock, Order, Portfolio,PortfolioStock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PortfolioStockSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = PortfolioStock
        fields = ['stock', 'quantity']

class PortfolioSerializer(serializers.ModelSerializer):
    stocks = PortfolioStockSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = ['user', 'stocks']
