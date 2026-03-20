from django import template

register = template.Library()

@register.filter
def zip(a, b):
    return zip(a, b)

@register.filter
def sum(items):
    return sum(items)

@register.filter
def mul(a, b):
    return a * b

@register.filter
def div(a, b):
    return a / b if b else 0

@register.filter
def filter(items, value):
    return [item for item in items if item == value]

@register.filter
def map(items, attr):
    return [getattr(item, attr) for item in items]

@register.filter
def compact(items):
    return [item for item in items if item] 