from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from .models import Doctor
from .serializers import (
    DoctorSerializer,
    DoctorListSerializer,
    DoctorDetailSerializer,
    DoctorSearchSerializer
)
from accounts.permissions import IsOwnerOrReadOnly


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating doctors.
    All authenticated users can view doctors, but only creators can modify.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'is_active']
    search_fields = ['name', 'email', 'specialization', 'qualification']
    ordering_fields = ['name', 'created_at', 'years_of_experience', 'consultation_fee']
    ordering = ['name']

    def get_queryset(self):
        """
        Return all active doctors for listing.
        """
        return Doctor.objects.filter(is_active=True)

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.request.method == 'GET':
            return DoctorListSerializer
        return DoctorSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new doctor.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = serializer.save()
        
        # Return detailed doctor data
        response_serializer = DoctorDetailSerializer(doctor)
        return Response({
            'message': 'Doctor created successfully',
            'doctor': response_serializer.data
        }, status=status.HTTP_201_CREATED)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific doctor.
    All users can view, but only creators can modify.
    """
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """
        Return all doctors.
        """
        return Doctor.objects.all()

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.request.method == 'GET':
            return DoctorDetailSerializer
        return DoctorSerializer

    def update(self, request, *args, **kwargs):
        """
        Update doctor information.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        doctor = serializer.save()

        # Return detailed doctor data
        response_serializer = DoctorDetailSerializer(doctor)
        return Response({
            'message': 'Doctor updated successfully',
            'doctor': response_serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete a doctor by setting is_active to False.
        """
        instance = self.get_object()
        
        # Check if doctor has active patient mappings
        active_mappings = instance.patient_mappings.filter(is_active=True).count()
        if active_mappings > 0:
            return Response({
                'error': f'Cannot delete doctor. Doctor has {active_mappings} active patient assignment(s). Please remove patient assignments first.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Soft delete
        instance.is_active = False
        instance.save()
        
        return Response({
            'message': 'Doctor deleted successfully'
        }, status=status.HTTP_200_OK)


class DoctorSearchView(generics.ListAPIView):
    """
    API endpoint for advanced doctor search.
    """
    serializer_class = DoctorSearchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'specialization', 'qualification', 'clinic_address']

    def get_queryset(self):
        """
        Return doctors with advanced filtering.
        """
        queryset = Doctor.objects.filter(is_active=True)
        
        # Additional query parameters
        specialization = self.request.query_params.get('specialization', None)
        min_experience = self.request.query_params.get('min_experience', None)
        max_experience = self.request.query_params.get('max_experience', None)
        max_fee = self.request.query_params.get('max_fee', None)
        min_fee = self.request.query_params.get('min_fee', None)
        available_day = self.request.query_params.get('available_day', None)
        
        if specialization:
            queryset = queryset.filter(specialization=specialization)
        
        if min_experience:
            queryset = queryset.filter(years_of_experience__gte=int(min_experience))
        
        if max_experience:
            queryset = queryset.filter(years_of_experience__lte=int(max_experience))
        
        if min_fee:
            queryset = queryset.filter(consultation_fee__gte=float(min_fee))
        
        if max_fee:
            queryset = queryset.filter(consultation_fee__lte=float(max_fee))
        
        if available_day:
            queryset = queryset.filter(available_days__icontains=available_day)
        
        return queryset.order_by('consultation_fee', '-years_of_experience')


class DoctorStatsView(generics.GenericAPIView):
    """
    API endpoint for doctor statistics.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get doctor statistics.
        """
        queryset = Doctor.objects.filter(is_active=True)
        
        total_doctors = queryset.count()
        
        # Specialization distribution
        specialization_stats = {}
        for choice in Doctor.SPECIALIZATION_CHOICES:
            count = queryset.filter(specialization=choice[0]).count()
            if count > 0:
                specialization_stats[choice[1]] = count
        
        # Experience distribution
        experience_groups = {
            '0-5 years': queryset.filter(years_of_experience__lte=5).count(),
            '6-15 years': queryset.filter(years_of_experience__gte=6, years_of_experience__lte=15).count(),
            '16-25 years': queryset.filter(years_of_experience__gte=16, years_of_experience__lte=25).count(),
            '25+ years': queryset.filter(years_of_experience__gt=25).count(),
        }
        
        # Fee statistics
        fee_stats = queryset.aggregate(
            avg_fee=Avg('consultation_fee'),
            min_fee=queryset.order_by('consultation_fee').first().consultation_fee if queryset.exists() else 0,
            max_fee=queryset.order_by('-consultation_fee').first().consultation_fee if queryset.exists() else 0
        )
        
        # Top specializations by patient count
        top_specializations = queryset.annotate(
            patient_count=Count('patient_mappings', filter=Q(patient_mappings__is_active=True))
        ).values('specialization', 'patient_count').order_by('-patient_count')[:5]
        
        return Response({
            'total_doctors': total_doctors,
            'specialization_distribution': specialization_stats,
            'experience_distribution': experience_groups,
            'fee_statistics': {
                'average_fee': round(fee_stats['avg_fee'] or 0, 2),
                'minimum_fee': fee_stats['min_fee'] or 0,
                'maximum_fee': fee_stats['max_fee'] or 0
            },
            'top_specializations_by_patients': [
                {
                    'specialization': dict(Doctor.SPECIALIZATION_CHOICES)[item['specialization']],
                    'patient_count': item['patient_count']
                }
                for item in top_specializations
            ]
        })


class DoctorsBySpecializationView(generics.ListAPIView):
    """
    API endpoint to get doctors by specialization.
    """
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return doctors filtered by specialization.
        """
        specialization = self.kwargs.get('specialization')
        return Doctor.objects.filter(
            specialization=specialization,
            is_active=True
        ).order_by('-years_of_experience')

    def list(self, request, *args, **kwargs):
        """
        List doctors with specialization info.
        """
        specialization = self.kwargs.get('specialization')
        
        # Validate specialization
        valid_specializations = [choice[0] for choice in Doctor.SPECIALIZATION_CHOICES]
        if specialization not in valid_specializations:
            return Response({
                'error': 'Invalid specialization',
                'valid_specializations': dict(Doctor.SPECIALIZATION_CHOICES)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        specialization_name = dict(Doctor.SPECIALIZATION_CHOICES)[specialization]
        
        return Response({
            'specialization': specialization_name,
            'count': queryset.count(),
            'doctors': serializer.data
        })
