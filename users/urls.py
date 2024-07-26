from django.urls import path
from rest_framework import routers
from users.views import OwnerViewSet, RetailStaffViewSet, AdminStaffViewSet, LoginView, LogoutView


router = routers.SimpleRouter()
router.register(r'api/v1/owner', OwnerViewSet, basename='owner')
router.register(r'api/v1/admin-staff', AdminStaffViewSet, basename='admin')
router.register(r'api/v1/retail-staff', RetailStaffViewSet, basename='retail')


urlpatterns = [
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls