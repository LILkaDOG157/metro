from rest_framework import serializers
from ..models import AssistanceRequest, Employee, MetroStation

class MetroStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetroStation
        fields = ['id', 'name', 'line', 'latitude', 'longitude']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'current_station', 'is_available']

class AssistanceRequestSerializer(serializers.ModelSerializer):
    start_station = MetroStationSerializer()
    end_station = MetroStationSerializer()
    passenger_type = serializers.CharField(source='passenger.get_type_display')
    
    class Meta:
        model = AssistanceRequest
        fields = ['id', 'passenger', 'passenger_type', 'start_station', 'end_station', 
                 'requested_time', 'status', 'created_at']