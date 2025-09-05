import django_filters
from .models import Patient


class PatientFilter(django_filters.FilterSet):
    """
    Filter class for Patient model with advanced filtering options.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    age_min = django_filters.NumberFilter(method='filter_age_min')
    age_max = django_filters.NumberFilter(method='filter_age_max')
    has_allergies = django_filters.BooleanFilter(method='filter_has_allergies')
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Patient
        fields = ['gender', 'is_active']

    def filter_age_min(self, queryset, name, value):
        """
        Filter patients with minimum age.
        """
        from datetime import date, timedelta
        if value:
            max_birth_date = date.today() - timedelta(days=value * 365.25)
            return queryset.filter(date_of_birth__lte=max_birth_date)
        return queryset

    def filter_age_max(self, queryset, name, value):
        """
        Filter patients with maximum age.
        """
        from datetime import date, timedelta
        if value:
            min_birth_date = date.today() - timedelta(days=value * 365.25)
            return queryset.filter(date_of_birth__gte=min_birth_date)
        return queryset

    def filter_has_allergies(self, queryset, name, value):
        """
        Filter patients based on whether they have allergies.
        """
        from django.db.models import Q
        if value:
            return queryset.exclude(Q(allergies__isnull=True) | Q(allergies=''))
        else:
            return queryset.filter(Q(allergies__isnull=True) | Q(allergies=''))
