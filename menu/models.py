from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Category(models.Model):
    """دسته‌بندی غذا: Breakfast / Lunch / Dinner ... (همان تب‌های تمپلیت)"""
    name = models.CharField('نام', max_length=120, unique=True)
    label = models.CharField('برچسب کوچک', max_length=60, default='Popular',
                             help_text='متن کوچک بالای نام تب، مثل Popular یا Special')
    icon = models.CharField('کلاس آیکون', max_length=80, default='fa-utensils',
                            help_text='مثلا: fa-coffee یا fa-hamburger')
    order = models.PositiveIntegerField('ترتیب', default=0)
    active = models.BooleanField('فعال', default=True)
    created_time = models.DateTimeField('زمان ایجاد', auto_now_add=True)
    updated_time = models.DateTimeField('آخرین ویرایش', auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu:category', args=[self.name])

    @property
    def dish_count(self):
        return self.dishes.filter(active=True).count()


class Dish(models.Model):
    """یک آیتم منو"""
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    MEAL_CHOICES = (
        (BREAKFAST, 'صبحانه'),
        (LUNCH, 'ناهار'),
        (DINNER, 'شام'),
    )

    title = models.CharField('نام غذا', max_length=255)
    description = models.TextField('توضیح کوتاه')
    price = models.DecimalField('قیمت', max_digits=10, decimal_places=2, default=0)
    image = models.ImageField('تصویر', upload_to='menu/', default='menu/default.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='dishes', verbose_name='دسته‌بندی')
    meal = models.CharField('وعده', max_length=20, choices=MEAL_CHOICES, default=DINNER)
    is_special = models.BooleanField('پیشنهاد ویژه', default=False)
    active = models.BooleanField('فعال', default=True)
    tag = TaggableManager('برچسب‌ها', blank=True)
    created_time = models.DateTimeField('زمان ایجاد', auto_now_add=True)
    updated_time = models.DateTimeField('آخرین ویرایش', auto_now=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'غذا'
        verbose_name_plural = 'غذاها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('menu:dish_detail', args=[self.pk])
