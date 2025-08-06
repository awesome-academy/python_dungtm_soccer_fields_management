from django import template
from django.utils.safestring import mark_safe
from soccer.enums import SoccerFieldStatus, SoccerFieldType
from django.utils.translation import gettext as _

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

@register.simple_tag
def field_type_badge(field_type):
    """Display a field type badge with appropriate icon and color."""
    if field_type == SoccerFieldType.INDOOR:
        badge_class = 'bg-info'
        icon = 'house'
        display_text = SoccerFieldType.choices[0][1]  # Get the display name from choices
    else:  # OUTDOOR
        badge_class = 'bg-success'
        icon = 'sun'
        display_text = SoccerFieldType.choices[1][1]  # Get the display name from choices
    
    html = f'''
        <span class="badge {badge_class}">
            <i class="bi bi-{icon} me-1"></i>{display_text}
        </span>
    '''
    return mark_safe(html)

@register.simple_tag
def star_rating_display(avg_rating, review_count=0):
    """Display star rating with optional review count."""
    if not avg_rating:
        return mark_safe('<small class="text-muted">' + _("No ratings yet") + '</small>')
    
    stars_html = ""
    for i in range(1, 6):
        if avg_rating >= i:
            stars_html += '<i class="bi bi-star-fill"></i>'
        elif avg_rating >= i - 0.5:
            stars_html += '<i class="bi bi-star-half"></i>'
        else:
            stars_html += '<i class="bi bi-star"></i>'
    
    count_html = f'<small class="text-muted ms-1">({review_count})</small>' if review_count else ''
    
    return mark_safe(f'<div class="text-warning">{stars_html}{count_html}</div>')

@register.inclusion_tag('soccer/partials/field_info.html')
def field_info(field, compact=False):
    """Render field information (address, phone, price) with icons."""
    return {
        'field': field,
        'compact': compact
    }
