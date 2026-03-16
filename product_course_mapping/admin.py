from django.contrib import admin

from product_course_mapping.models import ProductCourseMapping


@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'course', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
    list_filter = ['primary_mapping', 'is_active']
    search_fields = ['product__name', 'product__code', 'course__name', 'course__code']
