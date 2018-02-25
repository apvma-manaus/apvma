# Generated by Django 2.0 on 2018-02-23 15:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visitor',
            options={'ordering': ('-datetime', 'user', 'description'), 'verbose_name': 'Visita Autorizada', 'verbose_name_plural': 'Visitas Autorizadas'},
        ),
        migrations.RemoveField(
            model_name='visitor',
            name='arrival',
        ),
        migrations.RemoveField(
            model_name='visitor',
            name='exit',
        ),
        migrations.AddField(
            model_name='visitor',
            name='arrival_date',
            field=models.DateField(blank=True, null=True, verbose_name='data_chegada'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='arrival_time',
            field=models.TimeField(blank=True, null=True, verbose_name='hora chegada'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='card',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(60)], verbose_name='cartão'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='exit_date',
            field=models.DateField(blank=True, null=True, verbose_name='saída'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='exit_time',
            field=models.TimeField(blank=True, null=True, verbose_name='saída'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='description',
            field=models.TextField(max_length=50, verbose_name='nome / descrição'),
        ),
    ]