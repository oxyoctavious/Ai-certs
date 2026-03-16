from django.db import models
from django.db.models import Q

from certification.models import Certification
from common.models import PrimaryMappingBaseModel
from course.models import Course


class CourseCertificationMapping(PrimaryMappingBaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)

    class Meta(PrimaryMappingBaseModel.Meta):
        verbose_name = 'course certification mapping'
        verbose_name_plural = 'course certification mappings'
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'certification'],
                condition=Q(is_active=True),
                name='unique_active_course_certification_mapping',
            ),
            models.UniqueConstraint(
                fields=['course'],
                condition=Q(primary_mapping=True, is_active=True),
                name='unique_primary_certification_per_course',
            ),
        ]

    def __str__(self):
        return f'{self.course} -> {self.certification}'
