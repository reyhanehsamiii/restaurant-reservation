from datetime import datetime, timedelta, time

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Table(models.Model):
    INDOOR = 'indoor'
    OUTDOOR = 'outdoor'
    VIP = 'vip'
    LOCATION_CHOICES = (
        (INDOOR, 'سالن'),
        (OUTDOOR, 'فضای باز'),
        (VIP, 'وی‌آی‌پی'),
    )

    number = models.PositiveIntegerField('شماره میز', unique=True)
    capacity = models.PositiveIntegerField('ظرفیت', default=4,
                                           validators=[MinValueValidator(1), MaxValueValidator(20)])
    location = models.CharField('موقعیت', max_length=20, choices=LOCATION_CHOICES, default=INDOOR)
    active = models.BooleanField('فعال', default=True)

    class Meta:
        ordering = ['number']
        verbose_name = 'میز'
        verbose_name_plural = 'میزها'

    def __str__(self):
        return f'میز {self.number} ({self.capacity} نفره - {self.get_location_display()})'


class ReservationQuerySet(models.QuerySet):
    def blocking(self):
        """رزروهایی که میز را اشغال می‌کنند (لغو/رد شده‌ها میز را آزاد می‌کنند)."""
        return self.filter(status__in=[Reservation.PENDING, Reservation.CONFIRMED])

    def upcoming(self):
        return self.filter(date__gte=timezone.localdate()).order_by('date', 'time')

    def past(self):
        return self.filter(date__lt=timezone.localdate()).order_by('-date', '-time')


class Reservation(models.Model):
    """رزرو میز توسط کاربر یا مهمان"""
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    REJECTED = 'rejected'
    DONE = 'done'
    STATUS_CHOICES = (
        (PENDING, 'در انتظار تایید'),
        (CONFIRMED, 'تایید شده'),
        (CANCELLED, 'لغو شده توسط مشتری'),
        (REJECTED, 'رد شده'),
        (DONE, 'انجام شده'),
    )

    TIME_SLOTS = tuple(
        (time(h, m).strftime('%H:%M'), time(h, m).strftime('%H:%M'))
        for h in range(9, 23) for m in (0, 30)
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='reservations',
                             verbose_name='کاربر')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='reservations', verbose_name='میز')
    name = models.CharField('نام', max_length=255)
    email = models.EmailField('ایمیل')
    phone = models.CharField('تلفن', max_length=20, blank=True, default='')
    date = models.DateField('تاریخ')
    time = models.CharField('ساعت', max_length=5, choices=TIME_SLOTS, default='19:00')
    guests = models.PositiveIntegerField('تعداد نفرات', default=2,
                                         validators=[MinValueValidator(1), MaxValueValidator(20)])
    special_request = models.TextField('درخواست ویژه', blank=True, default='')
    status = models.CharField('وضعیت', max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_time = models.DateTimeField('زمان ثبت', auto_now_add=True)
    updated_time = models.DateTimeField('آخرین ویرایش', auto_now=True)

    objects = ReservationQuerySet.as_manager()

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزروها'

    def __str__(self):
        return f'{self.name} - {self.date} {self.time} ({self.guests} نفر)'

    @property
    def start_datetime(self):
        hour, minute = map(int, self.time.split(':'))
        return datetime.combine(self.date, time(hour, minute))

    @property
    def end_datetime(self):
        return self.start_datetime + timedelta(minutes=settings.RESERVATION_DURATION_MINUTES)

    @property
    def is_editable(self):
        """مشتری تا قبل از رسیدن زمان رزرو می‌تواند لغو کند."""
        return (self.status in (self.PENDING, self.CONFIRMED)
                and self.start_datetime > datetime.now())

    def overlaps_with(self, other_start):
        duration = timedelta(minutes=settings.RESERVATION_DURATION_MINUTES)
        return self.start_datetime < other_start + duration and other_start < self.end_datetime

    def clean(self):
        super().clean()
        errors = {}

        if self.date:
            today = timezone.localdate()
            if self.date < today:
                errors['date'] = 'تاریخ رزرو نمی‌تواند در گذشته باشد.'
            elif self.date > today + timedelta(days=settings.RESERVATION_MAX_DAYS_AHEAD):
                errors['date'] = (f'حداکثر تا {settings.RESERVATION_MAX_DAYS_AHEAD} '
                                  'روز آینده می‌توانید رزرو کنید.')

        if self.date and self.time and self.date == timezone.localdate():
            if self.start_datetime <= datetime.now():
                errors['time'] = 'این ساعت گذشته است. ساعت دیگری انتخاب کنید.'

        if self.table and self.guests and self.table.capacity < self.guests:
            errors['table'] = (f'ظرفیت میز {self.table.number} فقط '
                               f'{self.table.capacity} نفر است.')

        if self.table and self.date and self.time:
            clash = Reservation.objects.blocking().filter(
                table=self.table, date=self.date
            ).exclude(pk=self.pk)
            for other in clash:
                if other.overlaps_with(self.start_datetime):
                    errors['time'] = (f'میز {self.table.number} در ساعت {other.time} '
                                      'رزرو شده است. ساعت یا میز دیگری انتخاب کنید.')
                    break

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.table is None:
            self.table = self.find_free_table()
        super().save(*args, **kwargs)

    def find_free_table(self):
        """کوچک‌ترین میز خالی که ظرفیتش کافی باشد را پیدا می‌کند."""
        if not (self.date and self.time and self.guests):
            return None
        candidates = Table.objects.filter(active=True, capacity__gte=self.guests).order_by('capacity')
        busy = Reservation.objects.blocking().filter(date=self.date).exclude(pk=self.pk)
        for table in candidates:
            conflict = any(r.overlaps_with(self.start_datetime)
                           for r in busy.filter(table=table))
            if not conflict:
                return table
        return None
