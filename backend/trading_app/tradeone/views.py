from rest_framework import generics
from .models import Order,Portfolio,Stock,PortfolioStock
from .serializers import OrderSerializer,PortfolioSerializer,StockSerializer

class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Return only orders placed by the authenticated user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)  # Associate the order with the current user
        self.update_portfolio(order)

    def update_portfolio(self, order):
        user = order.user
        stock = order.stock
        quantity = order.quantity

        portfolio, created = Portfolio.objects.get_or_create(user=user)
        portfolio_stock, _ = PortfolioStock.objects.get_or_create(portfolio=portfolio, stock=stock)

        if order.order_type == Order.BUY:
            portfolio_stock.quantity += quantity
        elif order.order_type == Order.SELL:
            portfolio_stock.quantity -= quantity

        portfolio_stock.save()
        order.confirmed = True
        order.save()

class OrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class PortfolioDetailView(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def get_object(self):
        return Portfolio.objects.get(user=self.request.user)