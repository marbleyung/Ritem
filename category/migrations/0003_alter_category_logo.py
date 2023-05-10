# Generated by Django 4.2.1 on 2023-05-10 13:47

import category.models_services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_level_category_lft_category_rght_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='logo',
            field=models.FileField(blank=True, upload_to=category.models_services.category_logo_path, validators=[category.models_services.normal_category_logo_size]),
        ),
    ]
