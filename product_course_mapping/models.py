from django.db import models
from django.db.models import Q

from common.models import PrimaryMappingBaseModel
from course.models import Course
from product.models import Product


class ProductCourseMapping(PrimaryMappingBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta(PrimaryMappingBaseModel.Meta):
        verbose_name = 'product course mapping'
        verbose_name_plural = 'product course mappings'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'course'],
                condition=Q(is_active=True),
                name='unique_active_product_course_mapping',
            ),
            models.UniqueConstraint(
                fields=['product'],
                condition=Q(primary_mapping=True, is_active=True),
                name='unique_primary_course_per_product',
            ),
        ]

    def __str__(self):
        return f'{self.product} -> {self.course}'
