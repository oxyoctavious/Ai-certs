from rest_framework import serializers

from product_course_mapping.models import ProductCourseMapping


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = ProductCourseMapping
        fields = [
            'id',
            'product',
            'product_name',
            'course',
            'course_name',
            'primary_mapping',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'product_name', 'course_name']

    def validate(self, attrs):
        product = attrs.get('product', getattr(self.instance, 'product', None))
        course = attrs.get('course', getattr(self.instance, 'course', None))
        primary_mapping = attrs.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))
        is_active = attrs.get('is_active', getattr(self.instance, 'is_active', True))

        duplicate_queryset = ProductCourseMapping.objects.filter(product=product, course=course, is_active=True)
        if self.instance is not None:
            duplicate_queryset = duplicate_queryset.exclude(pk=self.instance.pk)
        if duplicate_queryset.exists():
            raise serializers.ValidationError('This product and course pair already exists.')

        if primary_mapping and is_active:
            primary_queryset = ProductCourseMapping.objects.filter(product=product, primary_mapping=True, is_active=True)
            if self.instance is not None:
                primary_queryset = primary_queryset.exclude(pk=self.instance.pk)
            if primary_queryset.exists():
                raise serializers.ValidationError('This product already has a primary course mapping.')

        return attrs
