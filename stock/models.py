from uuid import uuid4
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import date
from datetime import datetime
from django_prometheus.models import ExportModelOperationsMixin
import logging

log = logging.getLogger('main')

class Medication(models.Model, ExportModelOperationsMixin('medication')):
    """
    defines the model instance for each medication
    """
    drug_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        """
        string representation of the instance
        """
        return f'{self.name}, {self.price}, {self.quantity}'
