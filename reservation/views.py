from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ReservationForm
from .models import Reservation, Table


def booking(request):
    """صفحه booking.html — ثبت رزرو"""
    if request.method == 'POST':
        forms = ReservationForm(request.POST, user=request.user)
        if forms.is_valid():
            obj = forms.save()
            messages.success(
                request,
                f'رزرو شما برای {obj.date} ساعت {obj.time} ثبت شد '
                f'(میز {obj.table.number}). پس از تایید رستوران اطلاع‌رسانی می‌شود.'
            )
            if request.user.is_authenticated:
                return redirect('reservation:my_reservations')
            return redirect('reservation:booking')
        messages.error(request, 'ثبت رزرو انجام نشد؛ لطفا خطاها را بررسی کنید.')
    else:
        forms = ReservationForm(user=request.user)

    return render(request, 'reservation/booking.html', {'forms': forms})


@login_required
def my_reservations(request):
    """رزروهای کاربر لاگین‌شده"""
    reservations = Reservation.objects.filter(user=request.user)
    context = {
        'upcoming': reservations.upcoming(),
        'past': reservations.past(),
    }
    return render(request, 'reservation/my-reservations.html', context)


@login_required
@require_POST
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if reservation.is_editable:
        reservation.status = Reservation.CANCELLED
        reservation.save()
        messages.success(request, 'رزرو شما لغو شد.')
    else:
        messages.error(request, 'این رزرو قابل لغو نیست.')
    return redirect('reservation:my_reservations')


def availability(request):
    """صفحه ساده نمایش وضعیت میزها در یک تاریخ مشخص"""
    date = request.GET.get('date')
    rows = []
    if date:
        reserved = Reservation.objects.blocking().filter(date=date)
        for table in Table.objects.filter(active=True):
            rows.append({
                'table': table,
                'slots': reserved.filter(table=table).order_by('time'),
            })
    return render(request, 'reservation/availability.html', {'rows': rows, 'date': date})
