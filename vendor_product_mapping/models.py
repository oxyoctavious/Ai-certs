from django.db import models
from django.db.models import Q

from common.models import PrimaryMappingBaseModel
from product.models import Product
from vendor.models import Vendor


class VendorProductMapping(PrimaryMappingBaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta(PrimaryMappingBaseModel.Meta):
        verbose_name = 'vendor product mapping'
        verbose_name_plural = 'vendor product mappings'
        constraints = [
            models.UniqueConstraint(
                fields=['vendor', 'product'],
                condition=Q(is_active=True),
                name='unique_active_vendor_product_mapping',
            ),
            models.UniqueConstraint(
                fields=['vendor'],
                condition=Q(primary_mapping=True, is_active=True),
                name='unique_primary_product_per_vendor',
            ),
        ]

    def __str__(self):
        return f'{self.vendor} -> {self.product}'
