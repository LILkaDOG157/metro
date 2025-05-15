from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import AssistanceRequest, Passenger, Employee, Assignment, MetroStation
from .forms import PassengerForm, AssistanceRequestForm, EmployeeRegistrationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Q
import pandas as pd
from datetime import datetime

def home(request):
    stations = MetroStation.objects.all()
    # Получаем уникальные линии метро
    lines = stations.values_list('line', flat=True).distinct()
    # Группируем станции по линиям
    stations_by_line = {line: stations.filter(line=line) for line in lines}
    
    context = {
        'stations': stations,
        'stations_by_line': stations_by_line,
        'lines': lines,
    }
    return render(request, 'metro_app/home.html', context)

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'metro_app/register_employee.html', {'form': form})

class PassengerListView(LoginRequiredMixin, ListView):
    model = Passenger
    template_name = 'metro_app/passenger_list.html'
    context_object_name = 'passengers'

class PassengerCreateView(LoginRequiredMixin, CreateView):
    model = Passenger
    form_class = PassengerForm
    template_name = 'metro_app/passenger_form.html'
    success_url = reverse_lazy('passenger-list')

class AssistanceRequestListView(LoginRequiredMixin, ListView):
    model = AssistanceRequest
    template_name = 'metro_app/request_list.html'
    context_object_name = 'requests'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        try:
            employee = self.request.user.employee
            assignments = Assignment.objects.filter(employees=employee)
            return queryset.filter(
                Q(assignment__in=assignments) | 
                Q(status='pending') & 
                Q(start_station=employee.current_station)
            )
        except:
            return queryset.none()

class AssistanceRequestDetailView(LoginRequiredMixin, DetailView):
    model = AssistanceRequest
    template_name = 'metro_app/request_detail.html'

@login_required
def assign_request(request, pk):
    assistance_request = get_object_or_404(AssistanceRequest, pk=pk)
    
    if request.method == 'POST':
        employee = request.user.employee
        if not Assignment.objects.filter(request=assistance_request).exists():
            assignment = Assignment.objects.create(request=assistance_request)
            assignment.employees.add(employee)
            assistance_request.status = 'assigned'
            assistance_request.save()
            employee.is_available = False
            employee.save()
        return redirect('request-detail', pk=pk)
    
    return render(request, 'metro_app/assign_request.html', {'request': assistance_request})

@login_required
def complete_request(request, pk):
    assistance_request = get_object_or_404(AssistanceRequest, pk=pk)
    assignment = get_object_or_404(Assignment, request=assistance_request)
    
    if request.method == 'POST' and request.user.employee in assignment.employees.all():
        assistance_request.status = 'completed'
        assistance_request.save()
        assignment.end_time = datetime.now()
        assignment.save()
        for employee in assignment.employees.all():
            employee.is_available = True
            employee.current_station = assistance_request.end_station
            employee.save()
        return redirect('request-list')
    
    return render(request, 'metro_app/complete_request.html', {'request': assistance_request})

def load_stations(request):
    # Импорт станций из CSV (однократно)
    if MetroStation.objects.count() == 0:
        df = pd.read_csv('metro_app/data/moscow_metro_stations.csv')
        for _, row in df.iterrows():
            MetroStation.objects.create(
                name=row['Name'],
                line=row['Line'],
                latitude=row['Latitude'],
                longitude=row['Longitude']
            )
    return JsonResponse({'status': 'ok'})