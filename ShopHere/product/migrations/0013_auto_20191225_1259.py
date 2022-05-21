# Generated by Django 3.0.1 on 2019-12-25 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20191224_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='productform',
            name='image',
            field=models.ImageField(upload_to='product_images/'),
        ),
    ]
