from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Dish


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'label', 'icon', 'order', 'active', 'dish_count']
    list_editable = ['order', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(Dish)
class DishAdmin(SummernoteModelAdmin):
    list_display = ['thumbnail', 'title', 'category', 'meal', 'price', 'is_special', 'active']
    list_display_links = ['thumbnail', 'title']
    list_editable = ['price', 'is_special', 'active']
    list_filter = ['active', 'is_special', 'meal', 'category']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_time'
    summernote_fields = ('description',)

    @admin.display(description='تصویر')
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:45px;height:45px;object-fit:cover;border-radius:6px" />',
                               obj.image.url)
        return '-'
