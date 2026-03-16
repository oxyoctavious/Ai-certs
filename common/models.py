from django.db import models


class TimeStampedActiveModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NamedCodeDescriptionModel(TimeStampedActiveModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ['id']


class PrimaryMappingBaseModel(TimeStampedActiveModel):
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['id']
