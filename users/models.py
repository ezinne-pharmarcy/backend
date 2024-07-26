from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import date
from .managers import CustomUserManager
from datetime import datetime
from django_prometheus.models import ExportModelOperationsMixin
import logging
from django.contrib.auth.models import Group, Permission

log = logging.getLogger('main')

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ 
    Base User class.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateField(default=date.today())
    last_login = models.DateTimeField(default=datetime.now())
    is_authenticated = models.BooleanField(default=False)
    department = models.CharField(max_length=15, blank=True)
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Owner(ExportModelOperationsMixin('owner'), CustomUser):
    """ 
    Defines Owner model which inherits from the customUser class.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(null=True, max_length=15)
    date_of_birth = models.DateField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    is_store_admin = models.BooleanField(default=False)

# sort our get_absolute_url return reverse function
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """
        Returns the URL to access a particular user instance.
        """
        return reverse('user-detail', args=[str(self.id)])
    
    def __str__(self) -> str:
        """
        String representation of Individual User object.
        """
        return f'{self.username}'
    
    def save(self, *args, **kwargs):
        """
        Saves user class type.
        """
        log.info(f'saving owner with request data')
        self.is_staff = True
        super().save(*args, **kwargs)
        log.info(f'owner has been successfully saved')


class RetailStaff(ExportModelOperationsMixin('retail staff'), CustomUser):
    """ 
    Defines model for retail staff which inherits from the customUser class.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(null=True, max_length=15)
    date_of_birth = models.DateField(blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)

# sort our get_absolute_url return reverse function
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """
        Returns the URL to access a particular user instance.
        """
        return reverse('user-detail', args=[str(self.id)])
    
    def __str__(self) -> str:
        """
        String representation of Individual User object.
        """
        return f'{self.username}'
    
    def save(self, *args, **kwargs):
        """
        Saves user class type.
        """
        log.info(f'saving retail_staff with request data')
        super().save(*args, **kwargs)
        log.info(f'retail_staff has been successfully saved')


class AdminStaff(ExportModelOperationsMixin('admin staff'), CustomUser):
    """
    Defines model for admin staff which inherits from the customUser class.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(null=True, max_length=15)
    date_of_birth = models.DateField(blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)

# sort our get_absolute_url return reverse function
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """
        Returns the URL to access a particular user instance.
        """
        return reverse('user-detail', args=[str(self.id)])
    
    def __str__(self) -> str:
        """
        String representation of Individual User object.
        """
        return f'{self.username}, {self.profession}'
    
    def save(self, *args, **kwargs):
        """
        Saves user class type.
        """
        log.info(f'saving admin_staff with request data')
        super().save(*args, **kwargs)
        log.info(f'admin_staff has been successfully saved')

