from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('menu/', include('menu.urls')),
    path('reservation/', include('reservation.urls')),
    path('accounts/', include('accounts.urls')),
    path('captcha/', include('captcha.urls')),
    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'مدیریت رستوران Restoran'
admin.site.site_title = 'Restoran'
admin.site.index_title = 'پنل مدیریت'
