from rest_framework import serializers

from course_certification_mapping.models import CourseCertificationMapping


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    certification_name = serializers.CharField(source='certification.name', read_only=True)

    class Meta:
        model = CourseCertificationMapping
        fields = [
            'id',
            'course',
            'course_name',
            'certification',
            'certification_name',
            'primary_mapping',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'course_name', 'certification_name']

    def validate(self, attrs):
        course = attrs.get('course', getattr(self.instance, 'course', None))
        certification = attrs.get('certification', getattr(self.instance, 'certification', None))
        primary_mapping = attrs.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))
        is_active = attrs.get('is_active', getattr(self.instance, 'is_active', True))

        duplicate_queryset = CourseCertificationMapping.objects.filter(
            course=course,
            certification=certification,
            is_active=True,
        )
        if self.instance is not None:
            duplicate_queryset = duplicate_queryset.exclude(pk=self.instance.pk)
        if duplicate_queryset.exists():
            raise serializers.ValidationError('This course and certification pair already exists.')

        if primary_mapping and is_active:
            primary_queryset = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True, is_active=True)
            if self.instance is not None:
                primary_queryset = primary_queryset.exclude(pk=self.instance.pk)
            if primary_queryset.exists():
                raise serializers.ValidationError('This course already has a primary certification mapping.')

        return attrs
