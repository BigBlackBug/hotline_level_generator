# Generated by Django 3.0.7 on 2020-06-27 19:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200627_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='level_config',
            field=django.contrib.postgres.fields.jsonb.JSONField(max_length=1024),
        ),
    ]
