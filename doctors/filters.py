import django_filters
from .models import Doctor


class DoctorFilter(django_filters.FilterSet):
    """
    Filter class for Doctor model with advanced filtering options.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    min_experience = django_filters.NumberFilter(field_name='years_of_experience', lookup_expr='gte')
    max_experience = django_filters.NumberFilter(field_name='years_of_experience', lookup_expr='lte')
    min_fee = django_filters.NumberFilter(field_name='consultation_fee', lookup_expr='gte')
    max_fee = django_filters.NumberFilter(field_name='consultation_fee', lookup_expr='lte')
    available_day = django_filters.CharFilter(field_name='available_days', lookup_expr='icontains')
    qualification = django_filters.CharFilter(lookup_expr='icontains')
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Doctor
        fields = ['specialization', 'is_active']

    def filter_by_patient_count(self, queryset, name, value):
        """
        Filter doctors by minimum number of patients.
        """
        from django.db.models import Count
        return queryset.annotate(
            patient_count=Count('patient_mappings', filter=models.Q(patient_mappings__is_active=True))
        ).filter(patient_count__gte=value)
