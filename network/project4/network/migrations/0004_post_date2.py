# Generated by Django 5.0.3 on 2024-04-06 18:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date2',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
