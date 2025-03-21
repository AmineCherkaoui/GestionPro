# Generated by Django 5.2b1 on 2025-03-21 14:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type_de_societe', models.CharField(choices=[('SARL', 'Société à Responsabilité Limitée'), ('SAS', 'Société Anonyme Simplifiée'), ('SA', 'Société Anonyme'), ('SNC', 'Société en Nom Collectif'), ('SCI', 'Société Civile Immobilière')], max_length=4)),
                ('capital', models.DecimalField(decimal_places=2, max_digits=15)),
                ('gerant', models.CharField(max_length=255)),
                ('logo', models.ImageField(blank=True, upload_to='logos/')),
                ('location', models.CharField(max_length=255)),
                ('ice', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Please enter the right ICE number', regex='^\\d{15}$')])),
                ('tel', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Please enter the right phone number', regex='^[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}$')])),
                ('fax', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Please enter the right phone number', regex='^[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}$')])),
                ('address', models.TextField(blank=True)),
                ('bank_name', models.CharField(max_length=255)),
                ('numero_de_compte', models.CharField(max_length=16)),
                ('rib', models.CharField(max_length=24, validators=[django.core.validators.RegexValidator(message='Please enter the right RIB number', regex='^\\d{24}$')])),
                ('cnss', models.CharField(max_length=10)),
                ('patente', models.CharField(max_length=10)),
                ('IF', models.CharField(max_length=10)),
                ('RC', models.CharField(max_length=8)),
                ('hue', models.FloatField(blank=True, default=220)),
                ('saturation', models.FloatField(blank=True, default=80)),
            ],
        ),
    ]
