from rest_framework import serializers

from course.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        queryset = Course.objects.filter(code__iexact=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Course code must be unique.')
        return value


class CourseNestedSerializer(CourseSerializer):
    product_mappings = serializers.SerializerMethodField()
    certification_mappings = serializers.SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['product_mappings', 'certification_mappings']

    def get_product_mappings(self, obj):
        from product_course_mapping.models import ProductCourseMapping
        from product_course_mapping.serializers import ProductCourseMappingSerializer

        mappings = ProductCourseMapping.objects.filter(course=obj, is_active=True).select_related('product', 'course').order_by('id')
        return ProductCourseMappingSerializer(mappings, many=True).data

    def get_certification_mappings(self, obj):
        from course_certification_mapping.models import CourseCertificationMapping
        from course_certification_mapping.serializers import CourseCertificationMappingSerializer

        mappings = CourseCertificationMapping.objects.filter(course=obj, is_active=True).select_related('course', 'certification').order_by('id')
        return CourseCertificationMappingSerializer(mappings, many=True).data
