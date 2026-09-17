from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsTest(TestCase):
    def test_signup_creates_user(self):
        self.client.post(reverse('accounts:signup'), {
            'username': 'ali', 'email': 'ali@test.com',
            'password1': 'Str0ngPass!234', 'password2': 'Str0ngPass!234',
        })
        self.assertTrue(User.objects.filter(username='ali').exists())

    def test_my_reservations_requires_login(self):
        res = self.client.get(reverse('reservation:my_reservations'))
        self.assertEqual(res.status_code, 302)
