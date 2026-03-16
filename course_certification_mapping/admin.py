from django.contrib import admin

from course_certification_mapping.models import CourseCertificationMapping


@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
    list_filter = ['primary_mapping', 'is_active']
    search_fields = ['course__name', 'course__code', 'certification__name', 'certification__code']
