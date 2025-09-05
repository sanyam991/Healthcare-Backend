from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor
from .serializers import (
    PatientDoctorMappingSerializer,
    PatientDoctorMappingDetailSerializer,
    PatientDoctorMappingListSerializer,
    DoctorAssignmentSerializer,
    PatientDoctorsSerializer
)


class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating patient-doctor mappings.
    Users can only see mappings for their own patients.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_primary', 'is_active', 'doctor__specialization']
    search_fields = ['patient__name', 'doctor__name', 'notes']
    ordering_fields = ['assigned_at', 'patient__name', 'doctor__name']
    ordering = ['-assigned_at']

    def get_queryset(self):
        """
        Return mappings for patients created by the current user.
        """
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        ).select_related('patient', 'doctor', 'assigned_by')

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.request.method == 'GET':
            return PatientDoctorMappingListSerializer
        return PatientDoctorMappingSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new patient-doctor mapping.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mapping = serializer.save()
        
        # Return detailed mapping data
        response_serializer = PatientDoctorMappingDetailSerializer(mapping)
        return Response({
            'message': 'Doctor assigned to patient successfully',
            'mapping': response_serializer.data
        }, status=status.HTTP_201_CREATED)


class PatientDoctorMappingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific mapping.
    Users can only access mappings for their own patients.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return mappings for patients created by the current user.
        """
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        ).select_related('patient', 'doctor', 'assigned_by')

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.request.method == 'GET':
            return PatientDoctorMappingDetailSerializer
        return PatientDoctorMappingSerializer

    def update(self, request, *args, **kwargs):
        """
        Update mapping information.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        mapping = serializer.save()

        # Return detailed mapping data
        response_serializer = PatientDoctorMappingDetailSerializer(mapping)
        return Response({
            'message': 'Mapping updated successfully',
            'mapping': response_serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete a mapping by setting is_active to False.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        
        return Response({
            'message': 'Doctor removed from patient successfully'
        }, status=status.HTTP_200_OK)


class PatientDoctorsView(generics.RetrieveAPIView):
    """
    API endpoint to get all doctors assigned to a specific patient.
    """
    serializer_class = PatientDoctorsSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'patient_id'

    def get_queryset(self):
        """
        Return patients created by the current user.
        """
        return Patient.objects.filter(created_by=self.request.user)

    def get_object(self):
        """
        Get patient by patient_id from URL.
        """
        patient_id = self.kwargs.get('patient_id')
        return get_object_or_404(self.get_queryset(), id=patient_id)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_assign_doctor(request):
    """
    API endpoint for bulk assignment of a doctor to multiple patients.
    """
    serializer = DoctorAssignmentSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    
    doctor_id = serializer.validated_data['doctor_id']
    patient_ids = serializer.validated_data['patient_ids']
    notes = serializer.validated_data.get('notes', '')
    is_primary = serializer.validated_data.get('is_primary', False)
    
    doctor = Doctor.objects.get(id=doctor_id)
    patients = Patient.objects.filter(
        id__in=patient_ids,
        created_by=request.user,
        is_active=True
    )
    
    created_mappings = []
    skipped_mappings = []
    
    for patient in patients:
        # Check if mapping already exists
        existing_mapping = PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor,
            is_active=True
        ).exists()
        
        if not existing_mapping:
            mapping = PatientDoctorMapping.objects.create(
                patient=patient,
                doctor=doctor,
                assigned_by=request.user,
                notes=notes,
                is_primary=is_primary
            )
            created_mappings.append({
                'patient_name': patient.name,
                'mapping_id': mapping.id
            })
        else:
            skipped_mappings.append({
                'patient_name': patient.name,
                'reason': 'Doctor already assigned'
            })
    
    return Response({
        'message': f'Bulk assignment completed',
        'created_mappings': len(created_mappings),
        'skipped_mappings': len(skipped_mappings),
        'details': {
            'created': created_mappings,
            'skipped': skipped_mappings
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mapping_stats(request):
    """
    API endpoint for mapping statistics.
    """
    user_mappings = PatientDoctorMapping.objects.filter(
        patient__created_by=request.user,
        is_active=True
    )
    
    total_mappings = user_mappings.count()
    primary_mappings = user_mappings.filter(is_primary=True).count()
    
    # Patients with doctors
    patients_with_doctors = user_mappings.values('patient').distinct().count()
    total_patients = Patient.objects.filter(created_by=request.user, is_active=True).count()
    patients_without_doctors = total_patients - patients_with_doctors
    
    # Most assigned specializations
    specialization_stats = {}
    mappings_by_spec = user_mappings.values('doctor__specialization').annotate(
        count=Count('id')
    ).order_by('-count')
    
    for item in mappings_by_spec:
        spec_code = item['doctor__specialization']
        spec_name = dict(Doctor.SPECIALIZATION_CHOICES).get(spec_code, spec_code)
        specialization_stats[spec_name] = item['count']
    
    # Average doctors per patient
    avg_doctors_per_patient = round(total_mappings / patients_with_doctors, 2) if patients_with_doctors > 0 else 0
    
    return Response({
        'total_mappings': total_mappings,
        'primary_mappings': primary_mappings,
        'patients_with_doctors': patients_with_doctors,
        'patients_without_doctors': patients_without_doctors,
        'average_doctors_per_patient': avg_doctors_per_patient,
        'specialization_distribution': specialization_stats
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def set_primary_doctor(request, mapping_id):
    """
    API endpoint to set a doctor as primary for a patient.
    """
    try:
        mapping = PatientDoctorMapping.objects.get(
            id=mapping_id,
            patient__created_by=request.user,
            is_active=True
        )
        
        # Remove primary status from other doctors for this patient
        PatientDoctorMapping.objects.filter(
            patient=mapping.patient,
            is_primary=True
        ).update(is_primary=False)
        
        # Set this doctor as primary
        mapping.is_primary = True
        mapping.save()
        
        return Response({
            'message': f'Dr. {mapping.doctor.name} set as primary doctor for {mapping.patient.name}'
        })
        
    except PatientDoctorMapping.DoesNotExist:
        return Response({
            'error': 'Mapping not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)


class UnassignedPatientsView(generics.ListAPIView):
    """
    API endpoint to get patients without any doctor assignments.
    """
    serializer_class = PatientDoctorsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return patients without any active doctor assignments.
        """
        return Patient.objects.filter(
            created_by=self.request.user,
            is_active=True
        ).exclude(
            doctor_mappings__is_active=True
        )
