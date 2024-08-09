from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def zone_selected(zones):
    html = '<select name="zone">'
    for zone in zones:
        html += f'<option value="{zone[0]}">{zone[1]}</option>'
    html += '</select>'
    return mark_safe(html)