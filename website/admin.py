from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import SiteInfo, Service, Chef, Testimonial, Contact, Newsletter


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['brand', 'phone', 'email']

    def has_add_permission(self, request):
        # فقط یک رکورد اطلاعات سایت
        return not SiteInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'active']
    list_editable = ['order', 'active']
    search_fields = ['title', 'description']
    list_filter = ['active']


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'designation', 'order', 'active']
    list_editable = ['order', 'active']
    search_fields = ['full_name', 'designation']
    list_filter = ['active']


@admin.register(Testimonial)
class TestimonialAdmin(SummernoteModelAdmin):
    list_display = ['client_name', 'profession', 'active', 'created_time']
    list_filter = ['active']
    search_fields = ['client_name', 'message']
    date_hierarchy = 'created_time'
    summernote_fields = ('message',)
    actions = ['make_active']

    @admin.action(description='تایید نظرات انتخاب‌شده')
    def make_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f'{updated} نظر تایید شد.')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'is_read', 'created_time']
    list_filter = ['is_read']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_time'
    list_editable = ['is_read']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_time']
    search_fields = ['email']
