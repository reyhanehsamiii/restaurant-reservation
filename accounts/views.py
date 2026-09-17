from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignUpForm, LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('website:index')

    if request.method == 'POST':
        forms = LoginForm(request, data=request.POST)
        if forms.is_valid():
            login(request, forms.get_user())
            messages.success(request, f'خوش آمدید {request.user.username}!')
            return redirect(request.GET.get('next') or 'website:index')
        messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        forms = LoginForm()

    return render(request, 'accounts/login.html', {'forms': forms})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('website:index')

    if request.method == 'POST':
        forms = SignUpForm(request.POST)
        if forms.is_valid():
            user = forms.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
            return redirect('website:index')
        messages.error(request, 'لطفا خطاهای فرم را برطرف کنید.')
    else:
        forms = SignUpForm()

    return render(request, 'accounts/signup.html', {'forms': forms})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('website:index')
