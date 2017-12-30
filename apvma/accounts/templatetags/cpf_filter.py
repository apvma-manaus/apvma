from django import template


register = template.Library()

@register.filter(name='cpf')
def cpf(value):
    return '{}.{}.{}-{}'.format(value[:3], value[3:6], value[6:9], value[9:])


