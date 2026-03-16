from common.models import NamedCodeDescriptionModel


class Certification(NamedCodeDescriptionModel):
    class Meta(NamedCodeDescriptionModel.Meta):
        verbose_name = 'certification'
        verbose_name_plural = 'certifications'

    def __str__(self):
        return f'{self.name} ({self.code})'
