# Generated by Django 2.0 on 2018-01-12 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_auto_20180112_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(verbose_name='data solicitada'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='apartamento'),
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('date', 'spot')},
        ),
    ]
