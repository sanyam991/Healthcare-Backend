from django.urls import path
from .views import (
    PatientDoctorMappingListCreateView,
    PatientDoctorMappingDetailView,
    PatientDoctorsView,
    UnassignedPatientsView,
    bulk_assign_doctor,
    mapping_stats,
    set_primary_doctor
)

app_name = 'mappings'

urlpatterns = [
    # Main mapping endpoints
    path('', PatientDoctorMappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:pk>/', PatientDoctorMappingDetailView.as_view(), name='mapping-detail'),
    
    # Patient-specific endpoints
    path('<int:patient_id>/', PatientDoctorsView.as_view(), name='patient-doctors'),
    path('unassigned-patients/', UnassignedPatientsView.as_view(), name='unassigned-patients'),
    
    # Bulk operations
    path('bulk-assign/', bulk_assign_doctor, name='bulk-assign-doctor'),
    path('set-primary/<int:mapping_id>/', set_primary_doctor, name='set-primary-doctor'),
    
    # Statistics
    path('stats/', mapping_stats, name='mapping-stats'),
]
