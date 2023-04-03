"""
URL mappings for Store Products API.
"""
from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category'),
    path('product/', views.ProductList.as_view(), name='products'),
    path('product/<int:product_id>/',
         views.ProductDetail.as_view(), name='product-detail'),
    path('products/<int:category_id>/',
         views.ProductListByCategory.as_view(), name='product_category'),
    path('product-admin/', views.ProductAdminListView.as_view(), name='product-admin'),
    path('product-admin-detail/<int:pk>/', views.ProductAdminDetailView.as_view(),
         name='product-admin-detail'),
    path('order/', views.CustomerOrder.as_view(), name='order'),
    path('order/<int:pk>/<str:action>/',
         views.AddToCart.as_view(), name='add-to-cart'),
]
