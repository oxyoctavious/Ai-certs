from rest_framework import serializers

from vendor.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        queryset = Vendor.objects.filter(code__iexact=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Vendor code must be unique.')
        return value


class VendorNestedSerializer(VendorSerializer):
    product_mappings = serializers.SerializerMethodField()

    class Meta(VendorSerializer.Meta):
        fields = VendorSerializer.Meta.fields + ['product_mappings']

    def get_product_mappings(self, obj):
        from vendor_product_mapping.models import VendorProductMapping
        from vendor_product_mapping.serializers import VendorProductMappingSerializer

        mappings = VendorProductMapping.objects.filter(vendor=obj, is_active=True).select_related('vendor', 'product').order_by('id')
        return VendorProductMappingSerializer(mappings, many=True).data
