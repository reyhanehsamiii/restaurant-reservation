from django import forms
from django.utils import timezone
from captcha.fields import CaptchaField

from .models import Reservation, Table


class ReservationForm(forms.ModelForm):
    """فرم رزرو میز (همان فرم Book A Table Online تمپلیت)"""
    captcha = CaptchaField(label='کد امنیتی')

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'special_request']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'time': forms.Select(attrs={'class': 'form-select'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'special_request': forms.Textarea(attrs={'class': 'form-control',
                                                     'placeholder': 'Special Request',
                                                     'style': 'height: 100px'}),
        }
        labels = {
            'name': 'Your Name', 'email': 'Your Email', 'phone': 'Phone',
            'date': 'Date', 'time': 'Time', 'guests': 'No Of People',
            'special_request': 'Special Request',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['date'].initial = timezone.localdate()
        # اگر کاربر لاگین است، نام و ایمیلش را از قبل پر کن
        if user and user.is_authenticated and not self.is_bound:
            self.fields['name'].initial = user.get_full_name() or user.username
            self.fields['email'].initial = user.email

    def clean(self):
        """اعتبارسنجی سطح فرم: آیا اصلا میز خالی برای این زمان هست؟"""
        cleaned = super().clean()
        date = cleaned.get('date')
        t = cleaned.get('time')
        guests = cleaned.get('guests')

        if date and t and guests:
            instance = Reservation(date=date, time=t, guests=guests)
            if not Table.objects.filter(active=True, capacity__gte=guests).exists():
                raise forms.ValidationError(
                    f'متاسفانه میزی با ظرفیت {guests} نفر در رستوران وجود ندارد.')
            if instance.find_free_table() is None:
                raise forms.ValidationError(
                    'در این تاریخ و ساعت میز خالی نداریم. لطفا زمان دیگری انتخاب کنید.')
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        if self.user and self.user.is_authenticated:
            obj.user = self.user
        obj.full_clean(exclude=['table'])
        if commit:
            obj.save()
        return obj
