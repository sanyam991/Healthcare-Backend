from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Patient
from .serializers import (
    PatientSerializer,
    PatientListSerializer,
    PatientDetailSerializer
)
from accounts.permissions import IsAuthenticatedAndOwner


class PatientListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating patients.
    Users can only see patients they created.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'is_active']
    search_fields = ['name', 'email', 'phone_number']
    ordering_fields = ['name', 'created_at', 'date_of_birth']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return patients created by the current user.
        """
        return Patient.objects.filter(created_by=self.request.user)

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.request.method == 'GET':
            return PatientListSerializer
        return PatientSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new patient.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        
        # Return detailed patient data
        response_serializer = PatientDetailSerializer(patient)
        return Response({
            'message': 'Patient created successfully',
            'patient': response_serializer.data
        }, status=status.HTTP_201_CREATED)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific patient.
    Users can only access patients they created.
    """
    permission_classes = [IsAuthenticatedAndOwner]
    
    def get_queryset(self):
        """
        Return patients created by the current user.
        """
        return Patient.objects.filter(created_by=self.request.user)

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.request.method == 'GET':
            return PatientDetailSerializer
        return PatientSerializer

    def update(self, request, *args, **kwargs):
        """
        Update patient information.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        # Return detailed patient data
        response_serializer = PatientDetailSerializer(patient)
        return Response({
            'message': 'Patient updated successfully',
            'patient': response_serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete a patient by setting is_active to False.
        """
        instance = self.get_object()
        
        # Check if patient has active doctor mappings
        active_mappings = instance.doctor_mappings.filter(is_active=True).count()
        if active_mappings > 0:
            return Response({
                'error': f'Cannot delete patient. Patient has {active_mappings} active doctor assignment(s). Please remove doctor assignments first.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Soft delete
        instance.is_active = False
        instance.save()
        
        return Response({
            'message': 'Patient deleted successfully'
        }, status=status.HTTP_200_OK)


class PatientSearchView(generics.ListAPIView):
    """
    API endpoint for advanced patient search.
    """
    serializer_class = PatientListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'phone_number', 'medical_history', 'allergies']

    def get_queryset(self):
        """
        Return patients created by the current user with advanced filtering.
        """
        queryset = Patient.objects.filter(created_by=self.request.user, is_active=True)
        
        # Additional query parameters
        gender = self.request.query_params.get('gender', None)
        age_min = self.request.query_params.get('age_min', None)
        age_max = self.request.query_params.get('age_max', None)
        has_allergies = self.request.query_params.get('has_allergies', None)
        
        if gender:
            queryset = queryset.filter(gender=gender)
        
        if age_min or age_max:
            from datetime import date, timedelta
            today = date.today()
            
            if age_max:
                min_birth_date = today - timedelta(days=int(age_max) * 365.25)
                queryset = queryset.filter(date_of_birth__gte=min_birth_date)
            
            if age_min:
                max_birth_date = today - timedelta(days=int(age_min) * 365.25)
                queryset = queryset.filter(date_of_birth__lte=max_birth_date)
        
        if has_allergies is not None:
            if has_allergies.lower() == 'true':
                queryset = queryset.exclude(Q(allergies__isnull=True) | Q(allergies=''))
            else:
                queryset = queryset.filter(Q(allergies__isnull=True) | Q(allergies=''))
        
        return queryset


class PatientStatsView(generics.GenericAPIView):
    """
    API endpoint for patient statistics.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get patient statistics for the current user.
        """
        queryset = Patient.objects.filter(created_by=request.user)
        
        total_patients = queryset.count()
        active_patients = queryset.filter(is_active=True).count()
        inactive_patients = total_patients - active_patients
        
        # Gender distribution
        gender_stats = {}
        for choice in Patient.GENDER_CHOICES:
            count = queryset.filter(gender=choice[0], is_active=True).count()
            gender_stats[choice[1]] = count
        
        # Age distribution
        from datetime import date
        today = date.today()
        age_groups = {
            'Under 18': 0,
            '18-30': 0,
            '31-50': 0,
            '51-70': 0,
            'Over 70': 0
        }
        
        for patient in queryset.filter(is_active=True):
            age = patient.age
            if age < 18:
                age_groups['Under 18'] += 1
            elif age <= 30:
                age_groups['18-30'] += 1
            elif age <= 50:
                age_groups['31-50'] += 1
            elif age <= 70:
                age_groups['51-70'] += 1
            else:
                age_groups['Over 70'] += 1
        
        return Response({
            'total_patients': total_patients,
            'active_patients': active_patients,
            'inactive_patients': inactive_patients,
            'gender_distribution': gender_stats,
            'age_distribution': age_groups
        })
