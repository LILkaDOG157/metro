from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # Убедитесь, что импорт правильный!

router = DefaultRouter()
router.register(r'stations', views.MetroStationViewSet, basename='stations')  # ← Добавьте basename
router.register(r'requests', views.AssistanceRequestViewSet, basename='requests')  # ← И здесь

urlpatterns = [
    path('', include(router.urls)),
]