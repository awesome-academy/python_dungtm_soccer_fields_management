from django import template
from django.utils.safestring import mark_safe
from soccer.enums import SoccerFieldStatus

register = template.Library()

@register.simple_tag
def soccer_field_status_badge(field):
    status_class_map = {
        SoccerFieldStatus.ACTIVE: 'bg-success',
        SoccerFieldStatus.INACTIVE: 'bg-danger',
        SoccerFieldStatus.MAINTENANCE: 'bg-warning',
    }
    badge_class = status_class_map.get(field.status, 'bg-danger')
    html = (
        f'<span id="soccer-field-status-badge" class="badge {badge_class}">'
        f'{field.get_status_display()}</span>'
    )
    return mark_safe(html)
