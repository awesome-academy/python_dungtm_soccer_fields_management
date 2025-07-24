from django import template
from django.utils.safestring import mark_safe
from soccer.enums import RequestStatus

register = template.Library()

@register.simple_tag
def field_request_status_badge(fr):
    status_class_map = {
        RequestStatus.PENDING: 'bg-warning',
        RequestStatus.APPROVED: 'bg-success',
        RequestStatus.REJECTED: 'bg-danger',
        RequestStatus.CANCELLED: 'bg-secondary',
    }
    badge_class = status_class_map.get(fr.status, 'bg-danger')
    html = (
        f'<span id="field-request-status-badge" class="badge {badge_class}">'
        f'{fr.get_status_display()}</span>'
    )
    return mark_safe(html)
