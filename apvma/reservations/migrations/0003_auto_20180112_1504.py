# Generated by Django 2.0 on 2018-01-12 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20180112_0918'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ('date',), 'verbose_name': 'reserva', 'verbose_name_plural': 'reservas'},
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='expired',
        ),
        migrations.AddField(
            model_name='reservation',
            name='expires_on',
            field=models.DateTimeField(default='2018-01-01', editable=False, verbose_name='expira em'),
            preserve_default=False,
        ),
    ]
