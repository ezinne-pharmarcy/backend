from uuid import uuid4
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin
from django.utils import timezone
from users.models import RetailStaff
from stock.models import Medication


class Cart(models.Model, ExportModelOperationsMixin('cart')):
    """
    defines the cart model which manages each sales_cart
    """
    cart_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sales_staff = models.ForeignKey(RetailStaff, on_delete=models.CASCADE, verbose_name='Sales Staff')
    time_stamp = models.DateTimeField(default=timezone.now(), verbose_name='Order Timestamp')
    date = models.DateField(default=timezone.today(), verbose_name='Order Date')
    total_price = models.CharField(max_length=20, verbose_name='Total Price', default='0')

    def __str__(self):
        """
        string representation of the instance
        """
        return f'{self.sales_staff.email}, {self.time_stamp}, {self.total_price}'


class CartItem(models.Model):
    """
    defines the cart_item model which manages each medication_item in a sales_cart
    """
    cart_item_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    drug = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True)
    price = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = ['order', 'drug']

    def __str__(self):
        """
        string representation of the instance
        """
        return f'{self.order}, {self.drug}, {self.quantity}'


class Order(models.Model, ExportModelOperationsMixin('order')):
    """
    defines the order model which manages each sales_order
    """
    order_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sales_staff = models.ForeignKey(RetailStaff, on_delete=models.CASCADE, verbose_name='Sales Staff')
    time_stamp = models.DateTimeField(default=timezone.now(), verbose_name='Order Timestamp')
    date = models.DateField(default=timezone.today(), verbose_name='Order Date')
    total_price = models.CharField(max_length=20, verbose_name='Total Price', default='0')

    def __str__(self):
        """
        string representation of the instance
        """
        return f'{self.sales_staff.email}, {self.time_stamp}, {self.total_price}'


class OrderItem(models.Model):
    """
    defines the order_item model which manages each medication_item in a sales_order
    """
    order_item_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    drug = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True)
    price = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = ['order', 'drug']

    def __str__(self):
        """
        string representation of the instance
        """
        return f'{self.order}, {self.drug}, {self.quantity}'


