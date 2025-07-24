from django.db import models
from django.contrib.auth.models import User
from soccer.enums import (
    SoccerFieldStatus,
    OrderStatus,
    RequestType,
    RequestStatus,
    SoccerFieldType,
    OrderDurationChoice,
)
from soccer.constants import (
    MAX_LENGTH_16,
    MAX_LENGTH_32,
    MAX_LENGTH_128,
    MAX_LENGTH_256,
    DEFAULT_0,
    MAX_DIGITS,
    DECIMAL_PLACES    
)
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

# Create your models here.
class SoccerField(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_128)
    address = models.CharField(max_length=MAX_LENGTH_256)
    phone = models.CharField(max_length=MAX_LENGTH_32)
    email = models.EmailField()
    type = models.CharField(choices=SoccerFieldType.choices, default=SoccerFieldType.INDOOR)
    image = models.ImageField(upload_to='fields/', blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    status = models.CharField(
        max_length=MAX_LENGTH_16,
        choices=SoccerFieldStatus.choices,
        default=SoccerFieldStatus.ACTIVE
    )
    description = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Voucher(models.Model):
    code = models.CharField(max_length=MAX_LENGTH_32, unique=True)
    description = models.TextField(blank=True, null=True)
    discount_percent = models.PositiveSmallIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    min_price = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=DEFAULT_0)
    max_discount_amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=DEFAULT_0)
    rest_quantity = models.PositiveIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    soccer_field = models.ForeignKey(SoccerField, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=MAX_LENGTH_32,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    duration = models.PositiveIntegerField(choices=OrderDurationChoice.choices, default=OrderDurationChoice.DURATION_60)
    note = models.TextField(blank=True, null=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancel_reason = models.TextField(blank=True, null=True)

    @property
    def end_time(self):
        return self.time + timedelta(minutes=self.duration)

class Review(models.Model):
    soccer_field = models.ForeignKey(SoccerField, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)  # có thể cho phép không comment, nhưng thường nên bắt buộc
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('soccer_field', 'user')

class FieldRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=MAX_LENGTH_16,
        choices=RequestType.choices
    )
    status = models.CharField(
        max_length=MAX_LENGTH_16,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )
    soccer_field = models.ForeignKey(
        SoccerField, on_delete=models.SET_NULL, blank=True, null=True,
        help_text=_("The soccer field this request is related to.")
    )
    name = models.CharField(max_length=MAX_LENGTH_128, blank=True, null=True)
    address = models.CharField(max_length=MAX_LENGTH_256, blank=True, null=True)
    phone = models.CharField(max_length=MAX_LENGTH_32, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    type_field = models.CharField(
        choices=SoccerFieldType.choices, blank=True, null=True, max_length=MAX_LENGTH_16
    )
    image = models.ImageField(upload_to='fields/requests/', blank=True, null=True)
    price_per_hour = models.DecimalField(
        max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_create(self):
        return self.type == RequestType.ADD

    def is_update(self):
        return self.type == RequestType.UPDATE

    def is_delete(self):
        return self.type == RequestType.DELETE
