from django import template

register = template.Library()

@register.filter
def zip_lists(a, b):
    return zip(a, b)

@register.filter
def sum_values(items):
    try:
        return sum(items)
    except (TypeError, ValueError):
        return 0

@register.filter
def mul(a, b):
    try:
        return float(a) * float(b)
    except (TypeError, ValueError):
        return 0

@register.filter
def div(a, b):
    try:
        return float(a) / float(b) if float(b) else 0
    except (TypeError, ValueError):
        return 0

@register.filter
def filter_by_value(items, value):
    return [item for item in items if str(item) == str(value)]

@register.filter
def get_attr(items, attr):
    result = []
    for item in items:
        try:
            if '.' in attr:
                parts = attr.split('.')
                val = item
                for part in parts:
                    val = getattr(val, part)
                result.append(val)
            else:
                result.append(getattr(item, attr))
        except (AttributeError, TypeError):
            result.append(None)
    return result

@register.filter
def compact(items):
    return [item for item in items if item]

@register.filter
def length(items):
    return len(items)

@register.filter
def get_item(list_object, i):
    try:
        return list_object[i]
    except (IndexError, TypeError):
        return None 