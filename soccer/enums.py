from django.db import models
from django.utils.translation import gettext_lazy as _

class SoccerFieldStatus(models.TextChoices):
    ACTIVE = 'active', _('Active')
    INACTIVE = 'inactive', _('Inactive')
    MAINTENANCE = 'maintenance', _('Maintenance')

class OrderStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    CONFIRMED = 'confirmed', _('Confirmed')
    CANCELLED = 'cancelled', _('Cancelled')
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