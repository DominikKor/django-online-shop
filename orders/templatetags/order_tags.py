from django import template

register = template.Library()


@register.simple_tag
def addandfloatformat(a, b, decimal_points):
    return f"{a+b:.{decimal_points}f}"


@register.filter
def negative(a):
    return -a
