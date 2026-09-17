from django.db import models


class SiteInfo(models.Model):
    """اطلاعات کلی سایت که در هدر و فوتر همه صفحات استفاده می‌شود."""
    brand = models.CharField('نام رستوران', max_length=120, default='Restoran')
    address = models.CharField('آدرس', max_length=255, default='123 Street, New York, USA')
    phone = models.CharField('تلفن', max_length=50, default='+012 345 67890')
    email = models.EmailField('ایمیل', default='info@example.com')
    booking_email = models.EmailField('ایمیل رزرو', default='book@example.com')
    tech_email = models.EmailField('ایمیل پشتیبانی', default='tech@example.com')
    open_weekdays = models.CharField('ساعت کاری شنبه تا پنجشنبه', max_length=100, default='09AM - 09PM')
    open_weekend = models.CharField('ساعت کاری جمعه', max_length=100, default='10AM - 08PM')
    facebook = models.URLField('فیسبوک', blank=True, default='')
    twitter = models.URLField('توییتر', blank=True, default='')
    instagram = models.URLField('اینستاگرام', blank=True, default='')
    youtube = models.URLField('یوتیوب', blank=True, default='')
    map_embed = models.TextField('کد embed نقشه', blank=True, default='')

    class Meta:
        verbose_name = 'اطلاعات سایت'
        verbose_name_plural = 'اطلاعات سایت'

    def __str__(self):
        return self.brand

    def save(self, *args, **kwargs):
        """فقط یک رکورد اطلاعات سایت مجاز است (Singleton)."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Service(models.Model):
    """کارت‌های بخش خدمات (Master Chefs, Quality Food, ...)"""
    title = models.CharField('عنوان', max_length=120)
    description = models.TextField('توضیح')
    icon = models.CharField('کلاس آیکون', max_length=80, default='fa-utensils',
                            help_text='مثلا: fa-user-tie یا fa-cart-plus')
    order = models.PositiveIntegerField('ترتیب', default=0)
    active = models.BooleanField('فعال', default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'خدمت'
        verbose_name_plural = 'خدمات'

    def __str__(self):
        return self.title


class Chef(models.Model):
    """اعضای تیم / سرآشپزها"""
    full_name = models.CharField('نام و نام خانوادگی', max_length=120)
    designation = models.CharField('سمت', max_length=120, default='Chef')
    image = models.ImageField('تصویر', upload_to='team/', default='team/default.jpg')
    facebook = models.URLField('فیسبوک', blank=True, default='')
    twitter = models.URLField('توییتر', blank=True, default='')
    instagram = models.URLField('اینستاگرام', blank=True, default='')
    order = models.PositiveIntegerField('ترتیب', default=0)
    active = models.BooleanField('فعال', default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'سرآشپز'
        verbose_name_plural = 'تیم سرآشپزها'

    def __str__(self):
        return self.full_name


class Testimonial(models.Model):
    """نظرات مشتریان که در اسلایدر نمایش داده می‌شود."""
    client_name = models.CharField('نام مشتری', max_length=120)
    profession = models.CharField('شغل', max_length=120, blank=True, default='')
    message = models.TextField('متن نظر')
    image = models.ImageField('تصویر', upload_to='testimonial/', default='testimonial/default.jpg')
    active = models.BooleanField('تایید شده', default=False)
    created_time = models.DateTimeField('زمان ثبت', auto_now_add=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'نظر مشتری'
        verbose_name_plural = 'نظرات مشتریان'

    def __str__(self):
        return self.client_name


class Contact(models.Model):
    """پیام‌های فرم تماس با ما"""
    name = models.CharField('نام', max_length=255)
    email = models.EmailField('ایمیل')
    subject = models.CharField('موضوع', max_length=255)
    message = models.TextField('پیام')
    is_read = models.BooleanField('خوانده شده', default=False)
    created_time = models.DateTimeField('زمان ارسال', auto_now_add=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'

    def __str__(self):
        return f'{self.name} - {self.subject}'


class Newsletter(models.Model):
    """ایمیل‌های ثبت‌شده در خبرنامه فوتر"""
    email = models.EmailField('ایمیل', unique=True)
    created_time = models.DateTimeField('زمان عضویت', auto_now_add=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'عضو خبرنامه'
        verbose_name_plural = 'خبرنامه'

    def __str__(self):
        return self.email
