from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Dish, Category


def menu_list(request, **kwargs):

    dishes = Dish.objects.filter(active=True)
    active_filter = None

    if kwargs.get('cat'):
        dishes = dishes.filter(category__name=kwargs['cat'])
        active_filter = kwargs['cat']
    elif kwargs.get('meal'):
        dishes = dishes.filter(meal=kwargs['meal'])
        active_filter = kwargs['meal']
    elif kwargs.get('tag'):
        dishes = dishes.filter(tag__name=kwargs['tag'])
        active_filter = kwargs['tag']

    paginator = Paginator(dishes, 8)
    page_number = request.GET.get('page')
    dishes = paginator.get_page(page_number)

    context = {
        'dishes': dishes,
        'categories': Category.objects.filter(active=True),
        'active_filter': active_filter,
    }
    return render(request, 'menu/menu.html', context)


def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk, active=True)
    related = Dish.objects.filter(active=True, category=dish.category).exclude(pk=dish.pk)[:4]
    return render(request, 'menu/dish-detail.html', {'dish': dish, 'related': related})


def search(request):
    s = request.GET.get('s', '')
    dishes = Dish.objects.filter(active=True).filter(
        Q(title__icontains=s) | Q(description__icontains=s)
    ) if s else Dish.objects.none()

    context = {
        'dishes': dishes,
        'categories': Category.objects.filter(active=True),
        'search_term': s,
    }
    return render(request, 'menu/menu.html', context)
