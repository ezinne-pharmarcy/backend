from django.contrib import admin
from users.models import Owner, RetailStaff, AdminStaff
from django.contrib.auth.models import Group
# Register your models here.

admin.site.register(Owner)
admin.site.register(AdminStaff)
admin.site.register(RetailStaff)
# admin.site.unregister(Group)