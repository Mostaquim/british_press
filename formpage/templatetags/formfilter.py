from django.template import Library

register = Library()

def array_filter(value):
    if isinstance(value, list):
        if len(value) > 0:
            return " ".join(value)
    else:
        return value

def refine_name(value):
    ar = value.split('_')
    ar = [i.capitalize() for i in ar if len(i)>1]
    return " ".join(ar) + ":"

register.filter('array_filter', array_filter)
register.filter('refine_name', refine_name)