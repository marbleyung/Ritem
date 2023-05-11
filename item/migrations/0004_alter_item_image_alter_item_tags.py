# Generated by Django 4.2.1 on 2023-05-11 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_category_slug'),
        ('item', '0003_image_extension_alter_image_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ManyToManyField(blank=True, to='item.image'),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, to='category.tag'),
        ),
    ]
