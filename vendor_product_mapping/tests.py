from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Product
from vendor.models import Vendor
from vendor_product_mapping.models import VendorProductMapping
from vendor_product_mapping.serializers import VendorProductMappingSerializer


class VendorProductMappingAPITests(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Vendor A', code='V-A', description='Vendor')
        self.product_one = Product.objects.create(name='Product 1', code='P-1', description='Product 1')
        self.product_two = Product.objects.create(name='Product 2', code='P-2', description='Product 2')
        VendorProductMapping.objects.create(
            vendor=self.vendor,
            product=self.product_one,
            primary_mapping=True,
        )

    def test_duplicate_mapping_is_rejected(self):
        response = self.client.post(
            '/api/vendor-product-mappings/',
            {'vendor': self.vendor.id, 'product': self.product_one.id, 'primary_mapping': False},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_second_primary_mapping_for_same_vendor_is_rejected(self):
        response = self.client.post(
            '/api/vendor-product-mappings/',
            {'vendor': self.vendor.id, 'product': self.product_two.id, 'primary_mapping': True},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This vendor already has a primary product mapping.', str(response.data))


class VendorProductMappingSerializerTests(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Vendor B', code='V-B', description='Vendor')
        self.product_one = Product.objects.create(name='Product 1', code='PX-1', description='Product 1')
        self.product_two = Product.objects.create(name='Product 2', code='PX-2', description='Product 2')
        VendorProductMapping.objects.create(
            vendor=self.vendor,
            product=self.product_one,
            primary_mapping=True,
        )

    def test_primary_mapping_validation(self):
        serializer = VendorProductMappingSerializer(
            data={'vendor': self.vendor.id, 'product': self.product_two.id, 'primary_mapping': True}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('This vendor already has a primary product mapping.', str(serializer.errors))
