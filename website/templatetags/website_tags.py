from django import template
from ..models import Chef, Testimonial, Service

register = template.Library()


@register.simple_tag
def project_name():
    return 'Restoran - Django Restaurant Reservation'


@register.filter
def money(value):
    """۱۲۵۰۰۰ -> $125,000"""
    try:
        return '${:,.0f}'.format(float(value))
    except (TypeError, ValueError):
        return value


@register.inclusion_tag('includes/team.html')
def team_section(limit=4, title='Our Master Chefs'):
    return {'chefs': Chef.objects.filter(active=True)[:limit], 'section_title': title}


@register.inclusion_tag('includes/testimonial.html')
def testimonial_section():
    return {'testimonials': Testimonial.objects.filter(active=True)}


@register.inclusion_tag('includes/service.html')
def service_section():
    return {'services': Service.objects.filter(active=True)}
