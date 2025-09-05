from django.urls import path
from .views import (
    DoctorListCreateView,
    DoctorDetailView,
    DoctorSearchView,
    DoctorStatsView,
    DoctorsBySpecializationView
)

app_name = 'doctors'

urlpatterns = [
    # Main doctor endpoints
    path('', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    
    # Additional endpoints
    path('search/', DoctorSearchView.as_view(), name='doctor-search'),
    path('stats/', DoctorStatsView.as_view(), name='doctor-stats'),
    path('specialization/<str:specialization>/', DoctorsBySpecializationView.as_view(), name='doctors-by-specialization'),
]
