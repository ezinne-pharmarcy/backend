from uuid import uuid4
from django.db import models
from datetime import date
from datetime import datetime
from django_prometheus.models import ExportModelOperationsMixin
import logging
from django.utils import timezone
from users.models import RetailStaff, AdminStaff
from stock.models import Medication

log = logging.getLogger('main')

class Order(models.Model, ExportModelOperationsMixin('order')):
    """
    defines the order model which manages each sales_order
    """
    order_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sales_staff = models.ForeignKey(RetailStaff, on_delete=models.CASCADE, verbose_name='Sales Staff')
    time_stamp = models.DateTimeField(default=timezone.now(), verbose_name='Order Timestamp')
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


