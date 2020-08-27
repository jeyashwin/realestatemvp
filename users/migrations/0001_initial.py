# Generated by Django 2.2.5 on 2020-08-27 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LANDLORD',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('email_id', models.EmailField(max_length=254)),
                ('profile_picture', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='USER',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('email_id', models.EmailField(max_length=254)),
                ('profile_picture', models.ImageField(upload_to='')),
                ('college', models.TextField()),
            ],
        ),
    ]
