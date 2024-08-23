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

class UserTransactionSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source='stock.symbol')
    profit = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'type', 'quantity', 'price', 'profit', 'status', 'created_at', 'stock_symbol']  # Use 'type' instead of 'order_type'

    def get_profit(self, obj):
        if obj.type == 'sell':  
            # Get the corresponding buy order for profit calculation
            buy_order = Order.objects.filter(
                user=obj.user,
                stock=obj.stock,
                type='buy'  
            ).order_by('created_at').first()

            if buy_order:
                return obj.price - buy_order.price
        return None

class PortfolioStockSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioStock
        fields = ['stock', 'quantity', 'transactions']

    def get_transactions(self, obj):
        user = self.context['request'].user
        orders = Order.objects.filter(user=user, stock=obj.stock).order_by('-created_at')
        return UserTransactionSerializer(orders, many=True).data

class PortfolioSerializer(serializers.ModelSerializer):
    stocks = PortfolioStockSerializer(source='portfoliostock_set', many=True)

    class Meta:
        model = Portfolio
        fields = ['user', 'stocks']

