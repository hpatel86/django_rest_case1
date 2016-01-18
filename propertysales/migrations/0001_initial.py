# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PropertySale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postcode', models.CharField(max_length=8, verbose_name=b'PostCode', db_index=True)),
                ('property_type', models.CharField(max_length=1, verbose_name=b'Property Type', choices=[(b'D', b'Detached'), (b'S', b'Semi-Detached'), (b'T', b'Terraced'), (b'F', b'Flat/Maisonettes'), (b'O', b'Other')])),
                ('sale_date', models.DateField(verbose_name=b'Date of Transfer', db_index=True)),
                ('sale_price', models.PositiveIntegerField(verbose_name=b'Sale Price')),
                ('duration', models.CharField(max_length=1, verbose_name=b'Duration', choices=[(b'F', b'Freehold'), (b'L', b'Leasehold')])),
            ],
        ),
    ]
