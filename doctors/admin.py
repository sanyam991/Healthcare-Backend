from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Doctor model.
    """
    list_display = ('name', 'email', 'specialization', 'license_number', 'years_of_experience', 'consultation_fee', 'is_active')
    list_filter = ('specialization', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'license_number', 'specialization')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone_number')
        }),
        ('Professional Details', {
            'fields': ('license_number', 'specialization', 'years_of_experience', 'qualification')
        }),
        ('Practice Information', {
            'fields': ('clinic_address', 'consultation_fee', 'available_days', 'available_time')
        }),
        ('System Information', {
            'fields': ('created_by', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
