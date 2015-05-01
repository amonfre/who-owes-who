#https://stackoverflow.com/questions/401025/define-css-class-in-django-forms

from django import template

register = template.Library()

@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})
