"""
داده اولیه نمایشی:  python manage.py seed_demo
"""
from django.core.management.base import BaseCommand

from website.models import SiteInfo, Service, Chef, Testimonial
from menu.models import Category, Dish
from reservation.models import Table


class Command(BaseCommand):
    help = 'ساخت داده نمایشی برای رستوران (دسته‌بندی، غذا، میز، سرآشپز، خدمات)'

    def handle(self, *args, **options):
        SiteInfo.load()

        services = [
            ('Master Chefs', 'fa-user-tie', 'سرآشپزهای حرفه‌ای با سال‌ها تجربه در آشپزی بین‌المللی.'),
            ('Quality Food', 'fa-utensils', 'مواد اولیه تازه و روزانه، بدون نگهدارنده.'),
            ('Online Order', 'fa-cart-plus', 'سفارش و رزرو آنلاین تنها در چند کلیک.'),
            ('24/7 Service', 'fa-headset', 'پشتیبانی تلفنی در تمام ساعات شبانه‌روز.'),
        ]
        for i, (title, icon, desc) in enumerate(services):
            Service.objects.get_or_create(title=title, defaults={
                'icon': icon, 'description': desc, 'order': i})

        cats = [
            ('Breakfast', 'Popular', 'fa-coffee', 0),
            ('Lunch', 'Special', 'fa-hamburger', 1),
            ('Dinner', 'Lovely', 'fa-utensils', 2),
        ]
        cat_objs = {}
        for name, label, icon, order in cats:
            obj, _ = Category.objects.get_or_create(name=name, defaults={
                'label': label, 'icon': icon, 'order': order})
            cat_objs[name] = obj

        dishes = [
            ('Chicken Burger', 'Breakfast', 'breakfast', 115, 'برگر مرغ گریل شده با سس مخصوص و نان تازه.'),
            ('Pasta Alfredo', 'Lunch', 'lunch', 95, 'پاستا با سس آلفردو، قارچ و پارمزان.'),
            ('Grilled Salmon', 'Dinner', 'dinner', 180, 'فیله سالمون گریل با سبزیجات بخارپز.'),
            ('Caesar Salad', 'Lunch', 'lunch', 60, 'کاهو رومن، نان تست، پارمزان و سس سزار.'),
            ('Beef Steak', 'Dinner', 'dinner', 210, 'استیک راسته گوساله با سیب‌زمینی سرخ‌کرده.'),
            ('Pancake Stack', 'Breakfast', 'breakfast', 45, 'پنکیک با شربت افرا و کره.'),
            ('Margherita Pizza', 'Lunch', 'lunch', 120, 'پیتزا با سس گوجه، موزارلا و ریحان تازه.'),
            ('Lamb Chops', 'Dinner', 'dinner', 230, 'شیشلیک بره با ادویه مخصوص رستوران.'),
        ]
        for i, (title, cat, meal, price, desc) in enumerate(dishes):
            Dish.objects.get_or_create(title=title, defaults={
                'category': cat_objs[cat], 'meal': meal, 'price': price,
                'description': desc, 'is_special': i % 4 == 0,
                'image': f'menu/default.jpg',
            })

        chefs = [
            ('Ali Rahimi', 'Head Chef'),
            ('Sara Ahmadi', 'Pastry Chef'),
            ('Reza Karimi', 'Grill Master'),
            ('Mina Hosseini', 'Sous Chef'),
        ]
        for i, (name, role) in enumerate(chefs):
            Chef.objects.get_or_create(full_name=name, defaults={
                'designation': role, 'order': i})

        testimonials = [
            ('John Doe', 'Food Blogger', 'سرویس عالی و غذای فوق‌العاده. رزرو آنلاین خیلی راحت بود.'),
            ('Emma Watson', 'Designer', 'فضای دنج و کارکنان بسیار مودب. حتما دوباره می‌آیم.'),
            ('Karim N.', 'Engineer', 'میز دقیقا سر ساعت آماده بود، بدون هیچ انتظاری.'),
        ]
        for name, prof, msg in testimonials:
            Testimonial.objects.get_or_create(client_name=name, defaults={
                'profession': prof, 'message': msg, 'active': True})

        # میزها: ۴ تا ۲نفره، ۴ تا ۴نفره، ۲ تا ۶نفره، ۱ میز ۱۰ نفره VIP
        plan = [(2, 4, 'indoor'), (4, 4, 'indoor'), (6, 2, 'outdoor'), (10, 1, 'vip')]
        number = 1
        for capacity, count, location in plan:
            for _ in range(count):
                Table.objects.get_or_create(number=number, defaults={
                    'capacity': capacity, 'location': location})
                number += 1

        self.stdout.write(self.style.SUCCESS(
            f'داده نمایشی ساخته شد: {Dish.objects.count()} غذا، '
            f'{Table.objects.count()} میز، {Chef.objects.count()} سرآشپز.'))
