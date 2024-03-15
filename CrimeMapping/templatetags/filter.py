from django import template

register = template.Library()

@register.filter(name='get_filename')
def get_filename(value):
    return value.split('/')[-1]
