from rest_framework import serializers

from vendor_product_mapping.models import VendorProductMapping


class VendorProductMappingSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = VendorProductMapping
        fields = [
            'id',
            'vendor',
            'vendor_name',
            'product',
            'product_name',
            'primary_mapping',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'vendor_name', 'product_name']

    def validate(self, attrs):
        vendor = attrs.get('vendor', getattr(self.instance, 'vendor', None))
        product = attrs.get('product', getattr(self.instance, 'product', None))
        primary_mapping = attrs.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))
        is_active = attrs.get('is_active', getattr(self.instance, 'is_active', True))

        duplicate_queryset = VendorProductMapping.objects.filter(vendor=vendor, product=product, is_active=True)
        if self.instance is not None:
            duplicate_queryset = duplicate_queryset.exclude(pk=self.instance.pk)
        if duplicate_queryset.exists():
            raise serializers.ValidationError('This vendor and product pair already exists.')

        if primary_mapping and is_active:
            primary_queryset = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True, is_active=True)
            if self.instance is not None:
                primary_queryset = primary_queryset.exclude(pk=self.instance.pk)
            if primary_queryset.exists():
                raise serializers.ValidationError('This vendor already has a primary product mapping.')

        return attrs
