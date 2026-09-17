from django.contrib import admin
from django.utils.html import format_html
from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'capacity', 'location', 'active']
    list_editable = ['capacity', 'location', 'active']
    list_filter = ['location', 'active', 'capacity']
    search_fields = ['number']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'time', 'guests', 'table', 'colored_status', 'created_time']
    list_filter = ['status', 'date', 'table']
    search_fields = ['name', 'email', 'phone', 'special_request']
    date_hierarchy = 'date'
    list_display_links = ['name', 'date']
    autocomplete_fields = ['table']
    readonly_fields = ['created_time', 'updated_time']
    actions = ['confirm_reservations', 'reject_reservations', 'mark_done']
    fieldsets = (
        ('مشخصات مشتری', {'fields': ('user', 'name', 'email', 'phone')}),
        ('جزئیات رزرو', {'fields': ('date', 'time', 'guests', 'table', 'special_request')}),
        ('وضعیت', {'fields': ('status', 'created_time', 'updated_time')}),
    )

    @admin.display(description='وضعیت')
    def colored_status(self, obj):
        colors = {
            obj.PENDING: '#f39c12', obj.CONFIRMED: '#27ae60',
            obj.CANCELLED: '#7f8c8d', obj.REJECTED: '#c0392b', obj.DONE: '#2980b9',
        }
        return format_html('<b style="color:{}">{}</b>',
                           colors.get(obj.status, '#000'), obj.get_status_display())

    @admin.action(description='تایید رزروهای انتخاب‌شده')
    def confirm_reservations(self, request, queryset):
        updated = queryset.update(status=Reservation.CONFIRMED)
        self.message_user(request, f'{updated} رزرو تایید شد.')

    @admin.action(description='رد رزروهای انتخاب‌شده')
    def reject_reservations(self, request, queryset):
        updated = queryset.update(status=Reservation.REJECTED)
        self.message_user(request, f'{updated} رزرو رد شد.')

    @admin.action(description='علامت‌گذاری به عنوان انجام‌شده')
    def mark_done(self, request, queryset):
        updated = queryset.update(status=Reservation.DONE)
        self.message_user(request, f'{updated} رزرو انجام‌شده شد.')
