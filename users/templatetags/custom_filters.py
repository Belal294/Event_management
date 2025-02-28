# users/templatetags/custom_filters.py
from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def humanized_date(value):
    if value:
        if timezone.is_aware(value):
            value = timezone.localtime(value)

        today = timezone.localtime(timezone.now()).date()
        yesterday = today.replace(day=today.day - 1)

        if value.date() == today:
            return f"Today at {value.strftime('%I:%M %p')}"
        elif value.date() == yesterday:
            return f"Yesterday at {value.strftime('%I:%M %p')}"
        else:
            return f"{value.date().strftime('%B %d')}, {value.strftime('%I:%M %p')}"
    return "No login record available"
