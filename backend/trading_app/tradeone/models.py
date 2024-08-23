from django.db import models

from authentication.models import CustomUser


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100) 

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0) 

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.user} - {self.type} {self.quantity} {self.stock.symbol}"
    



class Portfolio(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, through='PortfolioStock')

class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()