from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='soccer_home'),
    path('field/<int:pk>/', views.detail, name='soccer_field_detail'),
    path('field/<int:pk>/order', views.order_field, name='order_field'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
]
