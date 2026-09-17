from django.test import TestCase
from django.urls import reverse
from .models import Category, Dish


class MenuTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Breakfast')
        self.dish = Dish.objects.create(title='Chicken Burger', description='x',
                                        price=115, category=self.cat)

    def test_menu_page(self):
        res = self.client.get(reverse('menu:menu'))
        self.assertContains(res, 'Chicken Burger')

    def test_category_filter(self):
        res = self.client.get(reverse('menu:category', args=['Breakfast']))
        self.assertEqual(len(res.context['dishes']), 1)

    def test_inactive_dish_hidden(self):
        self.dish.active = False
        self.dish.save()
        res = self.client.get(reverse('menu:menu'))
        self.assertEqual(len(res.context['dishes']), 0)
