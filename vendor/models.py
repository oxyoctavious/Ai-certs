from common.models import NamedCodeDescriptionModel


class Vendor(NamedCodeDescriptionModel):
    class Meta(NamedCodeDescriptionModel.Meta):
        verbose_name = 'vendor'
        verbose_name_plural = 'vendors'

    def __str__(self):
        return f'{self.name} ({self.code})'
