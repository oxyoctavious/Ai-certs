from rest_framework import serializers

from certification.models import Certification


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        queryset = Certification.objects.filter(code__iexact=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Certification code must be unique.')
        return value


class CertificationNestedSerializer(CertificationSerializer):
    course_mappings = serializers.SerializerMethodField()

    class Meta(CertificationSerializer.Meta):
        fields = CertificationSerializer.Meta.fields + ['course_mappings']

    def get_course_mappings(self, obj):
        from course_certification_mapping.models import CourseCertificationMapping
        from course_certification_mapping.serializers import CourseCertificationMappingSerializer

        mappings = CourseCertificationMapping.objects.filter(certification=obj, is_active=True).select_related('course', 'certification').order_by('id')
        return CourseCertificationMappingSerializer(mappings, many=True).data
