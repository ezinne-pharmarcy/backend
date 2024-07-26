from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sales.urls')),
    # path('', include('core.urls')),
    path('', include('users.urls')),
    path('', include('stock.urls')),
    path('', include('reports.urls')),
]
