# Generated by Django 3.0 on 2019-12-18 18:44

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20191218_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
