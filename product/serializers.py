from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        queryset = Product.objects.filter(code__iexact=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Product code must be unique.')
        return value


class ProductNestedSerializer(ProductSerializer):
    vendor_mappings = serializers.SerializerMethodField()
    course_mappings = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['vendor_mappings', 'course_mappings']

    def get_vendor_mappings(self, obj):
        from vendor_product_mapping.models import VendorProductMapping
        from vendor_product_mapping.serializers import VendorProductMappingSerializer

        mappings = VendorProductMapping.objects.filter(product=obj, is_active=True).select_related('vendor', 'product').order_by('id')
        return VendorProductMappingSerializer(mappings, many=True).data

    def get_course_mappings(self, obj):
        from product_course_mapping.models import ProductCourseMapping
        from product_course_mapping.serializers import ProductCourseMappingSerializer

        mappings = ProductCourseMapping.objects.filter(product=obj, is_active=True).select_related('product', 'course').order_by('id')
        return ProductCourseMappingSerializer(mappings, many=True).data
