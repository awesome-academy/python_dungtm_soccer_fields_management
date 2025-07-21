from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='soccer_home'),
    path('field/<int:pk>/', views.detail, name='soccer_field_detail'),
    path('field/<int:pk>/order', views.order_field, name='order_field'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path("vouchers/", views.voucher_list_user, name="voucher_list"),
    path("vouchers/manage", views.voucher_list_admin, name="voucher_list_admin"),
    path("vouchers/add/", views.voucher_create, name="voucher_create"),
    path("vouchers/<int:pk>/edit/", views.voucher_edit, name="voucher_edit"),
    path("vouchers/<int:pk>/delete/", views.voucher_delete, name="voucher_delete"),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('order/<int:pk>/cancel/', views.order_cancel, name='order_cancel'),
    path('admin/orders/', views.all_orders, name='all_orders'),
    path('admin/order/<int:pk>/cancel/', views.admin_cancel_order, name='admin_cancel_order'),
    path('admin/order/<int:pk>/accept/', views.admin_accept_order, name='admin_accept_order'),
    path('admin/order/<int:pk>/', views.admin_order_detail, name='admin_order_detail'),
]
