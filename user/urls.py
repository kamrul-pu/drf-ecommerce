"""
URL mappings for User API.
"""
from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('customer/', views.CustomerProfile.as_view(), name='customer'),

]
