# Generated by Django 2.0 on 2018-01-21 12:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountability', '0002_auto_20180106_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountability',
            name='file',
            field=models.FileField(upload_to='accountability/', validators=[django.core.validators.FileExtensionValidator(['pdf'], 'O sistema só permite o upload de arquivos PDF.')]),
        ),
    ]
