# Restoran — سیستم رزرو رستوران با جنگو

پیاده‌سازی کامل تمپلیت **Restoran (HTML Codex)** روی Django 4.2، با همان ساختار و سطح پروژه‌ی Stand Blog.

## راه‌اندازی

```bash
python -m venv venv
source venv/bin/activate        # ویندوز: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo      # داده نمایشی: غذا، میز، سرآشپز، خدمات
python manage.py createsuperuser
python manage.py runserver
```

یک ادمین آماده هم در دیتابیس هست: `admin` / `admin1234`

## اپ‌ها

| اپ | مسئولیت |
|---|---|
| `website` | صفحه اصلی، درباره ما، خدمات، تیم، نظرات، تماس، خبرنامه، اطلاعات سایت |
| `menu` | دسته‌بندی و غذاها، فیلتر، جستجو، صفحه جزئیات غذا |
| `reservation` | میزها، رزروها، اعتبارسنجی، رزروهای من، وضعیت میزها |
| `accounts` | ورود، ثبت‌نام، خروج |

## آدرس‌ها

```
/                          صفحه اصلی (خدمات + منو + فرم رزرو + تیم + نظرات)
/about/  /service/  /team/  /testimonial/  /contact/
/menu/                     همه غذاها + صفحه‌بندی
/menu/category/<name>/     فیلتر دسته‌بندی
/menu/meal/<meal>/         فیلتر وعده
/menu/tag/<tag>/           فیلتر برچسب
/menu/dish/<pk>/           جزئیات غذا
/menu/search/?s=...        جستجو
/reservation/              فرم رزرو میز
/reservation/my/           رزروهای من (نیاز به ورود)
/reservation/cancel/<pk>/  لغو رزرو (POST)
/reservation/availability/ وضعیت میزها در یک تاریخ
/accounts/login|signup|logout/
/admin/
```

## منطق رزرو

- هر رزرو به مدت `RESERVATION_DURATION_MINUTES` (پیش‌فرض ۹۰ دقیقه) میز را اشغال می‌کند.
- اگر میز انتخاب نشود، `find_free_table()` **کوچک‌ترین میز خالی با ظرفیت کافی** را خودکار اختصاص می‌دهد.
- در `Reservation.clean()` این‌ها چک می‌شود: تاریخ گذشته، ساعت گذشته‌ی امروز، سقف روزهای آینده،
  ظرفیت میز، و تداخل زمانی با رزروهای دیگرِ همان میز.
- رزروهای `cancelled` و `rejected` میز را آزاد می‌کنند (`ReservationQuerySet.blocking()`).
- وضعیت‌ها: در انتظار تایید / تایید شده / لغو شده / رد شده / انجام شده — با اکشن‌های گروهی در ادمین.

## نکات فنی

- **تمپلیت‌تگ‌ها:** `menu_tabs`, `menu_categories`, `special_dishes`, `price_tag` (اپ menu) و
  `team_section`, `testimonial_section`, `service_section`, `money` (اپ website).
- **context processor:** `website.context_processors.site_info` — اطلاعات سایت در همه‌ی صفحات.
- **کپچا:** روی فرم رزرو و فرم تماس (`django-simple-captcha`).
- **Summernote:** برای توضیح غذاها و متن نظرات در ادمین.
- **taggit:** برچسب‌گذاری غذاها.
- بخش «Date & Time» تمپلیت به دو فیلد `date` (input type=date) و `time` (انتخاب از بازه‌های ۳۰ دقیقه‌ای
  ۰۹:۰۰ تا ۲۲:۳۰) تبدیل شده تا اعتبارسنجی سمت سرور قابل اتکا باشد.

## تست

```bash
python manage.py test
```
۱۳ تست: صفحات سایت، فیلتر منو، کپچای فرم تماس، تخصیص خودکار میز، جلوگیری از رزرو تکراری،
رد تاریخ گذشته، رعایت ظرفیت، و آزادسازی میز پس از لغو.
