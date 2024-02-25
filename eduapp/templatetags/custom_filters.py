from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.filter(name='first_line_safe')
def first_line_safe(value):
    lines = value.split('\n')
    first_line = lines[0] if lines else ""
    return mark_safe(first_line)
