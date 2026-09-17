from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

from menu.models import Category, Dish
from reservation.forms import ReservationForm
from .models import Service, Chef, Testimonial
from .forms import ContactForm, NewsletterForm


def index(request):
    """صفحه اصلی: خدمات + منوی تبی + فرم رزرو + تیم + نظرات"""
    context = {
        'services': Service.objects.filter(active=True)[:4],
        'categories': Category.objects.filter(active=True),
        'dishes': Dish.objects.filter(active=True),
        'chefs': Chef.objects.filter(active=True)[:4],
        'testimonials': Testimonial.objects.filter(active=True),
        'forms': ReservationForm(),
    }
    return render(request, 'website/index.html', context)


def about(request):
    context = {
        'chefs': Chef.objects.filter(active=True)[:4],
    }
    return render(request, 'website/about.html', context)


def service(request):
    context = {'services': Service.objects.filter(active=True)}
    return render(request, 'website/service.html', context)


def team(request):
    context = {'chefs': Chef.objects.filter(active=True)}
    return render(request, 'website/team.html', context)


def testimonial(request):
    context = {'testimonials': Testimonial.objects.filter(active=True)}
    return render(request, 'website/testimonial.html', context)


def contact(request):
    if request.method == 'POST':
        forms = ContactForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد.')
            return redirect('website:contact')
        messages.error(request, 'لطفا خطاهای فرم را برطرف کنید.')
    else:
        forms = ContactForm()
    return render(request, 'website/contact.html', {'forms': forms})


@require_POST
def newsletter(request):
    """عضویت در خبرنامه از فوتر"""
    forms = NewsletterForm(request.POST)
    if forms.is_valid():
        forms.save()
        messages.success(request, 'عضویت شما در خبرنامه ثبت شد.')
    else:
        messages.error(request, forms.errors.get('email', ['ایمیل نامعتبر است.'])[0])
    return redirect(request.META.get('HTTP_REFERER', '/'))
