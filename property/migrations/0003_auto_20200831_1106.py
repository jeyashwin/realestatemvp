# Generated by Django 2.2.5 on 2020-08-31 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_auto_20200828_1906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='lot_size',
        ),
        migrations.AddField(
            model_name='property',
            name='property_name',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='property_status',
            field=models.CharField(default='null', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='property_type',
            field=models.CharField(default='null', max_length=50),
            preserve_default=False,
        ),
    ]
