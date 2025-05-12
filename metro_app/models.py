from django.db import models
from django.contrib.auth.models import User

class MetroStation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    line = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return f"{self.name} ({self.line})"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_station = models.ForeignKey(MetroStation, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.current_station})"

class Passenger(models.Model):
    PASSENGER_TYPE_CHOICES = [
        ('visually_impaired', 'Слабовидящий'),
        ('wheelchair', 'Колясочник'),
    ]
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=PASSENGER_TYPE_CHOICES)
    has_luggage = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class AssistanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('assigned', 'Назначена'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    start_station = models.ForeignKey(MetroStation, related_name='start_requests', on_delete=models.CASCADE)
    end_station = models.ForeignKey(MetroStation, related_name='end_requests', on_delete=models.CASCADE)
    requested_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Запрос #{self.id} от {self.passenger.name}"

class Assignment(models.Model):
    request = models.OneToOneField(AssistanceRequest, on_delete=models.CASCADE)
    employees = models.ManyToManyField(Employee)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Назначение для запроса #{self.request.id}"