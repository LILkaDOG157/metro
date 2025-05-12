from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from metro_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_employee, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Пассажиры
    path('passengers/', views.PassengerListView.as_view(), name='passenger-list'),
    path('passengers/new/', views.PassengerCreateView.as_view(), name='passenger-create'),
    
    # Запросы
    path('requests/', views.AssistanceRequestListView.as_view(), name='request-list'),
    path('requests/<int:pk>/', views.AssistanceRequestDetailView.as_view(), name='request-detail'),
    path('requests/<int:pk>/assign/', views.assign_request, name='request-assign'),
    path('requests/<int:pk>/complete/', views.complete_request, name='request-complete'),
    
    # API
    path('api/', include('metro_app.api.urls')),
    
    # Инициализация данных
    path('load-stations/', views.load_stations, name='load-stations'),
]