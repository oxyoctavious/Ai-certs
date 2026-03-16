from rest_framework.test import APITestCase

from vendor.serializers import VendorSerializer
from vendor.models import Vendor


class VendorSerializerTests(APITestCase):
    def test_unique_code_validation(self):
        Vendor.objects.create(name='Vendor A', code='VENDOR-A', description='Vendor')
        serializer = VendorSerializer(data={'name': 'Vendor B', 'code': 'VENDOR-A', 'description': 'Duplicate'})

        self.assertFalse(serializer.is_valid())
        self.assertIn('code', serializer.errors)
