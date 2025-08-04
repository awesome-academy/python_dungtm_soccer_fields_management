from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from soccer.enums import OrderStatus

register = template.Library()

@register.inclusion_tag('soccer/partials/voucher_select.html')
def voucher_select(vouchers, form, date_format):
    """Render a voucher selection dropdown with associated details panel."""
    return {
        'vouchers': vouchers,
        'form': form,
        'DATE_FORMAT': date_format
    }

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

@register.filter
def order_status_badge(status):
    """Display an order status with appropriate color."""
    status_class_map = {
        OrderStatus.PENDING: 'bg-warning',
        OrderStatus.CONFIRMED: 'bg-primary',
        OrderStatus.COMPLETED: 'bg-success',
        OrderStatus.CANCELLED_BY_USER: 'bg-secondary',
        OrderStatus.CANCELLED_BY_ADMIN: 'bg-danger',
    }
    badge_class = status_class_map.get(status, 'bg-secondary')
    
    return mark_safe(f'<span class="badge {badge_class}">{OrderStatus(status).label}</span>')

@register.filter
def duration_display(duration_minutes):
    """Convert duration minutes to a readable format."""
    hours = duration_minutes // 60
    minutes = duration_minutes % 60
    
    if hours == 0:
        return f"{minutes} {'minute' if minutes == 1 else 'minutes'}"
    elif minutes == 0:
        return f"{hours} {'hour' if hours == 1 else 'hours'}"
    else:
        return f"{hours} {'hour' if hours == 1 else 'hours'} {minutes} {'minute' if minutes == 1 else 'minutes'}"

@register.inclusion_tag('soccer/partials/field_price.html')
def field_price(price, discount_percent=None, original_price=None):
    """Display a formatted field price with optional discount."""
    return {
        'price': price,
        'discount_percent': discount_percent,
        'original_price': original_price
    }

@register.inclusion_tag('soccer/partials/order_info.html')
def order_info(order):
    """Display comprehensive order information in a standardized format."""
    return {
        'order': order
    }
