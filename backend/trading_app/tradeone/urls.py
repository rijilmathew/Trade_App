from django.urls import path
from .views import  OrderRetrieveUpdateDestroy,StockListCreateView,OrderListCreateView,PortfolioDetailView

urlpatterns = [
    path('stocks/', StockListCreateView.as_view(), name='stock-list-create'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroy.as_view(), name='order-retrieve-update-destroy'),
    path('portfolio-detail/', PortfolioDetailView.as_view(), name='portfolio-list'),
]