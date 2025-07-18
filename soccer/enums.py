from django.db import models
from django.utils.translation import gettext_lazy as _

class SoccerFieldStatus(models.TextChoices):
    ACTIVE = 'active', _('Active')
    INACTIVE = 'inactive', _('Inactive')
    MAINTENANCE = 'maintenance', _('Maintenance')

class OrderStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    CONFIRMED = 'confirmed', _('Confirmed')
    CANCELLED_BY_USER = 'cancelled_by_user', _('Cancelled by User')
    CANCELLED_BY_ADMIN = 'cancelled_by_admin', _('Cancelled by Admin')
    COMPLETED = 'completed', _('Completed')

class RequestType(models.TextChoices):
    ADD = 'add', _('Add Field')
    UPDATE = 'update', _('Update Field')
    DELETE = 'delete', _('Delete Field')

class RequestStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    APPROVED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')

class SoccerFieldType(models.TextChoices):
    INDOOR = 'indoor', _('Indoor')
    OUTDOOR = 'outdoor', _('Outdoor')

class OrderDurationChoice(models.IntegerChoices):
    DURATION_60 = 60, _('60 minutes')
    DURATION_90 = 90, _('90 minutes')
    DURATION_120 = 120, _('120 minutes')
    DURATION_150 = 150, _('150 minutes')
    DURATION_180 = 180, _('180 minutes')