from django import template
from ..models import Dish, Category

register = template.Library()


@register.inclusion_tag('includes/menu-tabs.html')
def menu_tabs(limit=8):
    """
    بخش منوی تبی تمپلیت را می‌سازد: هر دسته‌بندی یک تب و غذاهایش داخل آن.
    استفاده:  {% load menu_tags %}{% menu_tabs %}
    """
    categories = Category.objects.filter(active=True)
    data = []
    for cat in categories:
        data.append({
            'category': cat,
            'dishes': cat.dishes.filter(active=True)[:limit],
        })
    return {'tabs': data}


@register.inclusion_tag('includes/menu-categories.html')
def menu_categories():
    """لیست دسته‌بندی‌ها همراه با تعداد غذای هر کدام (سایدبار)"""
    categories = Category.objects.filter(active=True)
    return {'categories': categories}


@register.simple_tag
def special_dishes(limit=3):
    return Dish.objects.filter(active=True, is_special=True)[:limit]


@register.filter
def price_tag(value):
    try:
        return '${:,.0f}'.format(float(value))
    except (TypeError, ValueError):
        return value
