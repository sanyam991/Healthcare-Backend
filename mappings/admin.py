from django.contrib import admin
from .models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    """
    Admin configuration for PatientDoctorMapping model.
    """
    list_display = ('patient', 'doctor', 'is_primary', 'assigned_by', 'assigned_at', 'is_active')
    list_filter = ('is_primary', 'is_active', 'assigned_at', 'doctor__specialization')
    search_fields = ('patient__name', 'doctor__name', 'patient__email', 'doctor__email')
    readonly_fields = ('assigned_at',)
    ordering = ('-assigned_at',)
    
    fieldsets = (
        ('Mapping Information', {
            'fields': ('patient', 'doctor', 'is_primary', 'notes')
        }),
        ('System Information', {
            'fields': ('assigned_by', 'is_active', 'assigned_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related to reduce database queries.
        """
        return super().get_queryset(request).select_related('patient', 'doctor', 'assigned_by')
