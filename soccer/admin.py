from django.contrib import admin
from .models import SoccerField, Voucher, Order, Rating, Comment, FieldRequest

@admin.register(SoccerField)
class SoccerFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'type', 'price_per_hour', 'status')
    list_filter = ('status', 'type')
    search_fields = ('name', 'address', 'phone', 'email')
    ordering = ('-id',)

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount_percent', 'valid_from', 'valid_to', 'min_price', 'max_discount_amount', 'rest_quantity')
    search_fields = ('code', 'description')
    list_filter = ('valid_from', 'valid_to')
    ordering = ('-valid_from',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'soccer_field', 'time', 'duration', 'status', 'voucher', 'created_at')
    list_filter = ('status', 'soccer_field')
    search_fields = ('user__username', 'soccer_field__name', 'note')
    date_hierarchy = 'time'
    ordering = ('-created_at',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'soccer_field', 'user', 'rate', 'created_at')
    list_filter = ('soccer_field', 'rate')
    search_fields = ('soccer_field__name', 'user__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'soccer_field', 'user', 'created_at')
    list_filter = ('soccer_field',)
    search_fields = ('comment', 'user__username', 'soccer_field__name')

@admin.register(FieldRequest)
class FieldRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'status', 'created_at')
    list_filter = ('type', 'status')
    search_fields = ('user__username', 'note')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
