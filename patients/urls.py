from django.urls import path
from .views import (
    PatientListCreateView,
    PatientDetailView,
    PatientSearchView,
    PatientStatsView
)

app_name = 'patients'

urlpatterns = [
    # Main patient endpoints
    path('', PatientListCreateView.as_view(), name='patient-list-create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    
    # Additional endpoints
    path('search/', PatientSearchView.as_view(), name='patient-search'),
    path('stats/', PatientStatsView.as_view(), name='patient-stats'),
]
