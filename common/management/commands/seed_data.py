from django.core.management.base import BaseCommand

from certification.models import Certification
from course.models import Course
from course_certification_mapping.models import CourseCertificationMapping
from product.models import Product
from product_course_mapping.models import ProductCourseMapping
from vendor.models import Vendor
from vendor_product_mapping.models import VendorProductMapping


class Command(BaseCommand):
    help = 'Seed sample vendors, products, courses, certifications, and mappings.'

    def handle(self, *args, **options):
        vendor, _ = Vendor.objects.get_or_create(
            code='VENDOR-001',
            defaults={'name': 'Open Learning Vendor', 'description': 'Primary sample vendor'},
        )
        product, _ = Product.objects.get_or_create(
            code='PRODUCT-001',
            defaults={'name': 'AI Foundations', 'description': 'Primary sample product'},
        )
        course, _ = Course.objects.get_or_create(
            code='COURSE-001',
            defaults={'name': 'Prompt Engineering', 'description': 'Primary sample course'},
        )
        certification, _ = Certification.objects.get_or_create(
            code='CERT-001',
            defaults={'name': 'Prompt Engineer Level 1', 'description': 'Primary sample certification'},
        )

        VendorProductMapping.objects.get_or_create(
            vendor=vendor,
            product=product,
            defaults={'primary_mapping': True},
        )
        ProductCourseMapping.objects.get_or_create(
            product=product,
            course=course,
            defaults={'primary_mapping': True},
        )
        CourseCertificationMapping.objects.get_or_create(
            course=course,
            certification=certification,
            defaults={'primary_mapping': True},
        )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully.'))
