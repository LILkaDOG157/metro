from rest_framework import viewsets
from ..models import AssistanceRequest, Assignment, MetroStation
from .serializers import AssistanceRequestSerializer, MetroStationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.utils import timezone

class MetroStationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetroStation.objects.all()
    serializer_class = MetroStationSerializer

class AssistanceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AssistanceRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = AssistanceRequest.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AssistanceRequest.objects.all()
        try:
            employee = user.employee
            assignments = Assignment.objects.filter(employees=employee)
            return AssistanceRequest.objects.filter(
                Q(assignment__in=assignments) | 
                Q(status='pending') & 
                Q(start_station=employee.current_station)
            )
        except:
            return AssistanceRequest.objects.none()
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        request_obj = self.get_object()
        employee = request.user.employee
        
        if request_obj.status != 'pending':
            return Response({'status': 'error', 'message': 'Заявка уже назначена'})
        
        assignment, created = Assignment.objects.get_or_create(request=request_obj)
        assignment.employees.add(employee)
        request_obj.status = 'assigned'
        request_obj.save()
        employee.is_available = False
        employee.save()
        
        return Response({'status': 'success'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        request_obj = self.get_object()
        employee = request.user.employee
        
        if request_obj.status != 'assigned' or employee not in request_obj.assignment.employees.all():
            return Response({'status': 'error', 'message': 'Невозможно завершить заявку'})
        
        request_obj.status = 'completed'
        request_obj.save()
        assignment = request_obj.assignment
        assignment.end_time = timezone.now()
        assignment.save()
        
        for emp in assignment.employees.all():
            emp.is_available = True
            emp.current_station = request_obj.end_station
            emp.save()
        
        return Response({'status': 'success'})