# Generated by Django 3.2.2 on 2021-05-24 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20210518_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='id',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=250, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='superCategory',
            field=models.IntegerField(choices=[(3, 'Tiles')], default=1),
        ),
    ]
