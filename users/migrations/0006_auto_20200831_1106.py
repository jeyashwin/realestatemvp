# Generated by Django 2.2.5 on 2020-08-31 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200828_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landlord',
            name='profile_picture',
            field=models.ImageField(blank=True, default='null', upload_to='images'),
            preserve_default=False,
        ),
    ]
