from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='soccer_home'),
    path('field/<int:pk>/', views.detail, name='soccer_field_detail'),
]
