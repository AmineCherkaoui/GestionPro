# Generated by Django 5.2b1 on 2025-03-23 21:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandevirement',
            name='rib',
            field=models.CharField(max_length=24, validators=[django.core.validators.MinLengthValidator(24, 'the rib must contain 24 numbers')], verbose_name='RIB'),
        ),
    ]
