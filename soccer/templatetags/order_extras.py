from django import template
from django.utils.safestring import mark_safe
from soccer.enums import OrderStatus

register = template.Library()

@register.simple_tag
def order_status_badge(order):
    status_class_map = {
        OrderStatus.PENDING: 'bg-warning',
        OrderStatus.CONFIRMED: 'bg-success',
        OrderStatus.COMPLETED: 'bg-secondary',
        OrderStatus.CANCELLED_BY_USER: 'bg-danger',
        OrderStatus.CANCELLED_BY_ADMIN: 'bg-danger',
    }
    badge_class = status_class_map.get(order.status, 'bg-danger')
    html = (
        f'<span id="order-status-badge" class="badge {badge_class}">'
        f'{order.get_status_display()}</span>'
    )
    return mark_safe(html)
