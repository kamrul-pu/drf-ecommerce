"""URL Mapping For Admin User."""
from django.urls import path
from . import views

app_name = 'admin_user'

urlpatterns = [
    path('product-admin/', views.ProductAdminList.as_view(), name='product-admin'),
    path('product-admin-detail/<int:pk>/', views.ProductAdminDetail.as_view(),
         name='product-admin-detail'),
    path('discount/', views.DiscountList.as_view(), name='discount'),
    path('discount-detail/<int:pk>/', views.DiscountDetail.as_view(),
         name='discount-detail'),
    path('orders/', views.AdminOrderList.as_view(), name='admin-orders'),
    path('order-details/<int:pk>/', views.AdminOrderDetail.as_view(),
         name='admin-order-detail'),
    path('tag-product/', views.TagProductList.as_view(), name='tag-product'),
]
