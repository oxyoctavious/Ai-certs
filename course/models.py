from common.models import NamedCodeDescriptionModel


class Course(NamedCodeDescriptionModel):
    class Meta(NamedCodeDescriptionModel.Meta):
        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def __str__(self):
        return f'{self.name} ({self.code})'
