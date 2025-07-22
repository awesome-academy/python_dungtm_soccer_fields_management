from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DateTimeField
from .models import Order, OrderStatus

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

