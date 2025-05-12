from django import forms
from .models import Passenger, AssistanceRequest, Employee, MetroStation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'phone', 'type', 'has_luggage', 'additional_info']
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': 3}),
        }

class AssistanceRequestForm(forms.ModelForm):
    class Meta:
        model = AssistanceRequest
        fields = ['passenger', 'start_station', 'end_station', 'requested_time']
        widgets = {
            'requested_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EmployeeRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=20)
    station = forms.ModelChoiceField(queryset=MetroStation.objects.all())
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            employee = Employee.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                current_station=self.cleaned_data['station']
            )
        return user