from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import MetroStation, Employee, Passenger, AssistanceRequest, Assignment

# Настройка заголовков админки
admin.site.site_header = _("Администрирование метро")
admin.site.site_title = _("Метро")
admin.site.index_title = _("Управление метро")

@admin.register(MetroStation)
class MetroStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'line', 'latitude', 'longitude')
    search_fields = ('name', 'line')
    list_filter = ('line',)
    list_display_links = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'line')
        }),
        (_('Координаты'), {
            'fields': ('latitude', 'longitude')
        }),
    )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_station', 'is_available', 'phone')
    list_filter = ('is_available', 'current_station')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    fieldsets = (
        (None, {
            'fields': ('user', 'current_station', 'is_available')
        }),
        (_('Контактная информация'), {
            'fields': ('phone',)
        }),
    )

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'type', 'has_luggage')
    list_filter = ('type', 'has_luggage')
    search_fields = ('name', 'phone')
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'type')
        }),
        (_('Дополнительная информация'), {
            'fields': ('has_luggage', 'additional_info')
        }),
    )

@admin.register(AssistanceRequest)
class AssistanceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger', 'start_station', 'end_station', 'status', 'requested_time')
    list_filter = ('status', 'start_station', 'end_station')
    search_fields = ('passenger__name', 'start_station__name', 'end_station__name')
    fieldsets = (
        (None, {
            'fields': ('passenger', 'start_station', 'end_station', 'requested_time')
        }),
        (_('Статус'), {
            'fields': ('status',)
        }),
    )

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('request', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
    search_fields = ('request__passenger__name',)
    fieldsets = (
        (None, {
            'fields': ('request', 'employees')
        }),
        (_('Время'), {
            'fields': ('start_time', 'end_time')
        }),
        (_('Дополнительно'), {
            'fields': ('notes',)
        }),
    )
