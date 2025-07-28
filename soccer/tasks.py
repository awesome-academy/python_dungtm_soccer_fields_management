from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DateTimeField
from .models import Order, OrderStatus
from django.contrib.auth.models import User
from datetime import timedelta
from celery import shared_task
from soccer.constants import MAX_ACTIVATE_DURATION_ACCOUNT_HOURS

@shared_task
def auto_complete_orders():
    now = timezone.now()

    try:
        orders_to_complete = Order.objects.annotate(
            end_time=ExpressionWrapper(
                F('time') + F('duration') * 60,  
                output_field=DateTimeField()
            )
        ).filter(
            status=OrderStatus.CONFIRMED,
            end_time__lte=now
        )

        count = orders_to_complete.update(status=OrderStatus.COMPLETED)
        return f"Completed {count} orders."
    except Exception as e:
        print(f"[auto_complete_orders] ERROR: {e}")
        return "Error completing orders."

@shared_task
def delete_expired_inactive_users():
    expire_hours = MAX_ACTIVATE_DURATION_ACCOUNT_HOURS
    deadline = timezone.now() - timedelta(hours=expire_hours)
    users = User.objects.filter(is_active=False, date_joined__lt=deadline)
    count = users.count()
    users.delete()
    return f"Deleted {count} expired, inactive users."
