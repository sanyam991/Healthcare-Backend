from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin configuration for Patient model.
    """
    list_display = ('name', 'email', 'phone_number', 'gender', 'age', 'created_by', 'created_at', 'is_active')
    list_filter = ('gender', 'is_active', 'created_at', 'created_by')
    search_fields = ('name', 'email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'age')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone_number')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'address')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'allergies', 'emergency_contact_name', 'emergency_contact_phone')
        }),
        ('System Information', {
            'fields': ('created_by', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def age(self, obj):
        return obj.age
    age.short_description = 'Age'
