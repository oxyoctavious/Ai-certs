from django.contrib import admin

from vendor_product_mapping.models import VendorProductMapping


@admin.register(VendorProductMapping)
class VendorProductMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'product', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
    list_filter = ['primary_mapping', 'is_active']
    search_fields = ['vendor__name', 'vendor__code', 'product__name', 'product__code']
