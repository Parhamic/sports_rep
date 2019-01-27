from django import template
from django.utils import timezone

register = template.Library()


@register.filter("is_going")
def is_going(value):
    return (value.start_time <= timezone.localtime().time() and value.end_time > timezone.localtime().time())


@register.filter("not_today")
def not_today(value):
    return (value != timezone.localdate())
