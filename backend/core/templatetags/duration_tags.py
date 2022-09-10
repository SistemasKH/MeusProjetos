from django import template

register = template.Library()


@register.filter('duration_to_hours')
def duration_to_hours(value):
    '''
    Converte duration em horas.
    '''
    horas = value.days * 24
    resto = value.days - value.seconds
    return f'{horas} h {resto}'
