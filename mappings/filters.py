import django_filters
from .models import PatientDoctorMapping


class PatientDoctorMappingFilter(django_filters.FilterSet):
    """
    Filter class for PatientDoctorMapping model.
    """
    patient_name = django_filters.CharFilter(field_name='patient__name', lookup_expr='icontains')
    doctor_name = django_filters.CharFilter(field_name='doctor__name', lookup_expr='icontains')
    specialization = django_filters.ChoiceFilter(
        field_name='doctor__specialization',
        choices=lambda: [(choice[0], choice[1]) for choice in PatientDoctorMapping._meta.get_field('doctor').related_model.SPECIALIZATION_CHOICES]
    )
    assigned_after = django_filters.DateFilter(field_name='assigned_at', lookup_expr='gte')
    assigned_before = django_filters.DateFilter(field_name='assigned_at', lookup_expr='lte')
    assigned_by = django_filters.CharFilter(field_name='assigned_by__name', lookup_expr='icontains')

    class Meta:
        model = PatientDoctorMapping
        fields = ['is_primary', 'is_active']
