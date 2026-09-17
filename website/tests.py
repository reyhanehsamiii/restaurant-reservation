from django.test import TestCase
from django.urls import reverse
from .models import Contact


class WebsitePagesTest(TestCase):
    def test_index_ok(self):
        self.assertEqual(self.client.get(reverse('website:index')).status_code, 200)

    def test_contact_page_ok(self):
        self.assertEqual(self.client.get(reverse('website:contact')).status_code, 200)

    def test_contact_requires_captcha(self):
        self.client.post(reverse('website:contact'), {
            'name': 'Ali', 'email': 'a@b.com', 'subject': 'Hi', 'message': 'Test',
        })
        self.assertEqual(Contact.objects.count(), 0)
