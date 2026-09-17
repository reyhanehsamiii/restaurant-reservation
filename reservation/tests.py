from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Table, Reservation


class ReservationRulesTest(TestCase):
    def setUp(self):
        self.t2 = Table.objects.create(number=1, capacity=2)
        self.t6 = Table.objects.create(number=2, capacity=6)
        self.tomorrow = timezone.localdate() + timedelta(days=1)

    def test_auto_assign_smallest_table(self):
        r = Reservation.objects.create(name='Ali', email='a@b.com',
                                       date=self.tomorrow, time='19:00', guests=2)
        self.assertEqual(r.table, self.t2)

    def test_double_booking_blocked(self):
        Reservation.objects.create(name='Ali', email='a@b.com',
                                   date=self.tomorrow, time='19:00', guests=2, table=self.t2)
        clash = Reservation(name='Reza', email='r@b.com', date=self.tomorrow,
                            time='19:30', guests=2, table=self.t2)
        with self.assertRaises(ValidationError):
            clash.full_clean(exclude=['table'])

    def test_past_date_rejected(self):
        r = Reservation(name='Ali', email='a@b.com',
                        date=timezone.localdate() - timedelta(days=1), time='19:00', guests=2)
        with self.assertRaises(ValidationError):
            r.full_clean(exclude=['table'])

    def test_capacity_respected(self):
        r = Reservation(name='Ali', email='a@b.com', date=self.tomorrow,
                        time='19:00', guests=5, table=self.t2)
        with self.assertRaises(ValidationError):
            r.full_clean(exclude=['table'])

    def test_cancelled_frees_the_table(self):
        first = Reservation.objects.create(name='Ali', email='a@b.com', date=self.tomorrow,
                                           time='19:00', guests=2, table=self.t2)
        first.status = Reservation.CANCELLED
        first.save()
        second = Reservation(name='Reza', email='r@b.com', date=self.tomorrow,
                             time='19:00', guests=2, table=self.t2)
        second.full_clean(exclude=['table'])  # نباید خطا بدهد
