from django.core.validators import FileExtensionValidator
from django.db import models


class Assembly(models.Model):
    file = models.FileField('ata da assembleia', upload_to='assembly/minutes/',
                            validators=[FileExtensionValidator(['pdf'], 'O sistema só permite o upload de arquivos PDF.')])
    date = models.DateField('data da assembleia')

    class Meta:
        verbose_name = 'Ata de Assembleia'
        verbose_name_plural = 'Atas de Assembleia'