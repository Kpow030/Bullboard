from django import template

register = template.Library()

@register.filter
def censor_filter(value):
    censor_mat = ['мудак', 'лох', 'сука', 'блять', 'чурка']
    words = value.split()
    filtered_words = [word for word in words if word.lower() not in censor_mat]
    return '*'.join(filtered_words)