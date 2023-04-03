"""URL Mapping For Admin User."""
from django.urls import path
from . import views

app_name = 'admin_user'

urlpatterns = [
    path('product-admin/', views.ProductAdminList.as_view(), name='product-admin'),
    path('product-admin-detail/<int:pk>/', views.ProductAdminDetail.as_view(),
         name='product-admin-detail'),
]
