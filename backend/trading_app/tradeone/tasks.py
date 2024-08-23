from datetime import timezone
from celery import shared_task
import requests
from .models import Stock,Order
from django.db import transaction
import requests
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_stock_data():
    logger.info("Starting update_stock_data task")
    url = 'https://api.example.com/stocks'
    logger.info("Fetching stock data from URL: %s", url)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
    else:
        try:
            data = response.json()
        except ValueError as json_err:
            logger.error(f"JSON decode error: {json_err}")
            return
        
        for stock_data in data:
            symbol = stock_data.get('symbol')
            price = stock_data.get('price')
            quantity = stock_data.get('quantity')

            if not symbol or price is None or quantity is None:
                logger.warning(f"Invalid data received: {stock_data}")
                continue

            stock, created = Stock.objects.update_or_create(
                symbol=symbol,
                defaults={'price': price, 'quantity': quantity}
            )
            if not created:
                stock.last_updated = timezone.now()
                stock.save()

        logger.info("Stock data update complete")


@shared_task
def execute_orders():
    buy_orders = Order.objects.filter(order_type=Order.BUY, status='pending').order_by('price')
    sell_orders = Order.objects.filter(order_type=Order.SELL, status='pending').order_by('-price')
    
    for buy_order in buy_orders:
        for sell_order in sell_orders:
            if buy_order.stock == sell_order.stock and buy_order.price >= sell_order.price:
                quantity_to_trade = min(buy_order.quantity, sell_order.quantity)
                
                with transaction.atomic():
                    buy_order.quantity -= quantity_to_trade
                    sell_order.quantity -= quantity_to_trade
                    
                    if buy_order.quantity == 0:
                        buy_order.status = 'executed'
                    if sell_order.quantity == 0:
                        sell_order.status = 'executed'
                    
                    buy_order.save()
                    sell_order.save()
                    
                    # Update stock quantities and user balances
                    stock = buy_order.stock
                    stock.quantity -= quantity_to_trade
                    stock.save()
                    
                    # Notify users (you'll need to implement this)
                    # notify_user(buy_order.user)
                    # notify_user(sell_order.user)


@shared_task
def run_all_tasks():
    update_stock_data.delay()
    execute_orders.delay()