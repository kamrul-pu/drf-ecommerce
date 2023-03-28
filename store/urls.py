"""
URL mappings for Store Products API.
"""
from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:product_id>/',
         views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:category_id>/',
         views.ProductListByCategory.as_view(), name='product_category'),
]
