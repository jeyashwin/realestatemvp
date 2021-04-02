# Generated by Django 3.1.2 on 2021-03-11 16:59

from django.db import migrations
import imagekit.models.fields
import property.utils


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_auto_20210114_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyimage',
            name='imagePath',
            field=imagekit.models.fields.ProcessedImageField(upload_to=property.utils.unique_file_path_generator, verbose_name='Image'),
        ),
    ]