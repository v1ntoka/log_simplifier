from django import template
from django.forms import BoundField

register = template.Library()


# @register.filter
# def add_class(field: BoundField, css):
#     attrs = field.field.a
#     attrs['class'] = f"{attrs.get('class', '')}{' ' * attrs.get('class', '')}{css}"
#     return field.as_widget(attrs={'class': css})
