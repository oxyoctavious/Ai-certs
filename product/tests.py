from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Product
from vendor.models import Vendor
from vendor_product_mapping.models import VendorProductMapping
from product.serializers import ProductSerializer


class ProductFilterAPITests(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Vendor A', code='VENDOR-A', description='Vendor')
        self.product = Product.objects.create(name='Product A', code='PRODUCT-A', description='Product')
        self.other_product = Product.objects.create(name='Product B', code='PRODUCT-B', description='Product')
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product, primary_mapping=True)

    def test_vendor_id_filter_returns_only_related_products(self):
        response = self.client.get(f'/api/products/?vendor_id={self.vendor.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.product.id)

    def test_nested_product_endpoint_includes_related_mappings(self):
        response = self.client.get(f'/api/products/{self.product.id}/nested/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['vendor_mappings']), 1)
        self.assertEqual(response.data['vendor_mappings'][0]['vendor'], self.vendor.id)


class ProductSerializerTests(APITestCase):
    def test_unique_code_validation(self):
        Product.objects.create(name='Product A', code='PRODUCT-A1', description='Existing')
        serializer = ProductSerializer(data={'name': 'Product B', 'code': 'PRODUCT-A1', 'description': 'Duplicate'})

        self.assertFalse(serializer.is_valid())
        self.assertIn('code', serializer.errors)
