from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class MetroStation(models.Model):
    name = models.CharField(_('Название'), max_length=100, unique=True)
    line = models.CharField(_('Линия'), max_length=50)
    latitude = models.FloatField(_('Широта'))
    longitude = models.FloatField(_('Долгота'))
    
    class Meta:
        verbose_name = _('Станция метро')
        verbose_name_plural = _('Станции метро')
    
    def __str__(self):
        return f"{self.name} ({self.line})"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    current_station = models.ForeignKey(MetroStation, on_delete=models.SET_NULL, null=True, verbose_name=_('Текущая станция'))
    is_available = models.BooleanField(_('Доступен'), default=True)
    phone = models.CharField(_('Телефон'), max_length=20)
    
    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.current_station})"

class Passenger(models.Model):
    PASSENGER_TYPE_CHOICES = [
        ('visually_impaired', _('Слабовидящий')),
        ('wheelchair', _('Колясочник')),
    ]
    
    name = models.CharField(_('Имя'), max_length=100)
    phone = models.CharField(_('Телефон'), max_length=20)
    type = models.CharField(_('Тип пассажира'), max_length=20, choices=PASSENGER_TYPE_CHOICES)
    has_luggage = models.BooleanField(_('Есть багаж'), default=False)
    additional_info = models.TextField(_('Дополнительная информация'), blank=True)
    
    class Meta:
        verbose_name = _('Пассажир')
        verbose_name_plural = _('Пассажиры')
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class AssistanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Ожидает')),
        ('assigned', _('Назначена')),
        ('in_progress', _('В процессе')),
        ('completed', _('Завершена')),
        ('cancelled', _('Отменена')),
    ]
    
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, verbose_name=_('Пассажир'))
    start_station = models.ForeignKey(MetroStation, related_name='start_requests', on_delete=models.CASCADE, verbose_name=_('Станция отправления'))
    end_station = models.ForeignKey(MetroStation, related_name='end_requests', on_delete=models.CASCADE, verbose_name=_('Станция прибытия'))
    requested_time = models.DateTimeField(_('Запрошенное время'))
    status = models.CharField(_('Статус'), max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('Запрос на помощь')
        verbose_name_plural = _('Запросы на помощь')
    
    def __str__(self):
        return f"Запрос #{self.id} от {self.passenger.name}"

class Assignment(models.Model):
    request = models.OneToOneField(AssistanceRequest, on_delete=models.CASCADE, verbose_name=_('Запрос'))
    employees = models.ManyToManyField(Employee, verbose_name=_('Сотрудники'))
    start_time = models.DateTimeField(_('Время начала'))
    end_time = models.DateTimeField(_('Время окончания'), null=True, blank=True)
    notes = models.TextField(_('Заметки'), blank=True)
    
    class Meta:
        verbose_name = _('Назначение')
        verbose_name_plural = _('Назначения')
    
    def __str__(self):
        return f"Назначение для запроса #{self.request.id}"