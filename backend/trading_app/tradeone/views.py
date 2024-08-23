from rest_framework import generics
from rest_framework.response import Response
from .models import Order,Portfolio,Stock,PortfolioStock
from .serializers import OrderSerializer,PortfolioSerializer,StockSerializer
from rest_framework.permissions import IsAuthenticated

class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

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
        portfolio_stock, _ = PortfolioStock.objects.get_or_create(portfolio=portfolio, stock=stock,quantity=quantity)

        if order.type == 'buy':
            portfolio_stock.quantity += quantity
        elif order.type == 'sell':
            portfolio_stock.quantity -= quantity
        
        if portfolio_stock.quantity < 0:
             portfolio_stock.quantity = 0

        portfolio_stock.save()
        order.save()

class OrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class PortfolioDetailView(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated] 

    def get_object(self):
        try:
            # Attempt to retrieve the portfolio for the authenticated user
            return Portfolio.objects.get(user=self.request.user)
        except Portfolio.DoesNotExist:
            # Return a 404 response if the portfolio does not exist
             return Response({"detail": "No portfolio found for the authenticated user."}, status=204)