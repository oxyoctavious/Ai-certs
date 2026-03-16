from common.models import NamedCodeDescriptionModel


class Product(NamedCodeDescriptionModel):
    class Meta(NamedCodeDescriptionModel.Meta):
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'{self.name} ({self.code})'
