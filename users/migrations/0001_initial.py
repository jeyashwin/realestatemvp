# Generated by Django 3.1.2 on 2020-12-28 11:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactEmail', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Contact US',
            },
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.CharField(help_text='Type of Interest. eg Partying, Sports etc', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userType', models.CharField(choices=[('student', 'Student'), ('seller', 'Seller')], max_length=50)),
                ('student', models.BooleanField(default=False, editable=False)),
                ('landLord', models.BooleanField(default=False, editable=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='US')),
                ('university', models.CharField(max_length=50)),
                ('classYear', models.IntegerField(validators=[django.core.validators.MinValueValidator(2010, 'Minimum year 2010'), django.core.validators.MaxValueValidator(2030, 'Maximum year 2030')])),
                ('profilePicture', models.ImageField(default='uploads/avatar/profile_avatar.png', upload_to=users.models.profile_image_file_path)),
                ('fbLink', models.URLField(blank=True, max_length=250, null=True)),
                ('snapLink', models.URLField(blank=True, max_length=250, null=True)),
                ('instaLink', models.URLField(blank=True, max_length=250, null=True)),
                ('twitterLink', models.URLField(blank=True, max_length=250, null=True)),
                ('sleepScheduleFrom', models.TimeField(blank=True, null=True)),
                ('sleepScheduleTo', models.TimeField(blank=True, null=True)),
                ('studyHourFrom', models.TimeField(blank=True, null=True)),
                ('studyHourTo', models.TimeField(blank=True, null=True)),
                ('tobaccoUsage', models.CharField(blank=True, choices=[('never', 'Never'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('occasionally', 'Occasionally')], max_length=100)),
                ('alcoholUsage', models.CharField(blank=True, choices=[('never', 'Never'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('occasionally', 'Occasionally')], max_length=100)),
                ('cleanliness', models.CharField(blank=True, choices=[('daily', 'Daily'), ('occasionally', 'Occasionally')], max_length=100)),
                ('guests', models.CharField(blank=True, choices=[('daily', 'Daily'), ('occasionally', 'Occasionally')], max_length=100)),
                ('emailVerified', models.BooleanField(default=False)),
                ('phoneVerified', models.BooleanField(default=False)),
                ('livingHabitsLater', models.BooleanField(default=False)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('interests', models.ManyToManyField(to='users.Interest')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.usertype')),
            ],
        ),
        migrations.CreateModel(
            name='UserLandLord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='US')),
                ('emailVerified', models.BooleanField(default=False)),
                ('phoneVerified', models.BooleanField(default=False)),
                ('profilePicture', models.ImageField(default='uploads/avatar/profile_avatar.png', upload_to=users.models.profile_image_file_path)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.usertype')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='US')),
                ('wrongAttemptCount', models.IntegerField(default=5)),
                ('resendCodeCount', models.IntegerField(default=3)),
                ('is_blocked', models.BooleanField(default=False)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('userObj', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InviteCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inviteCode', models.CharField(max_length=200, unique=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_invite', to='users.userstudent')),
                ('studentJoined', models.ManyToManyField(blank=True, related_name='joined_user', to='users.UserStudent')),
            ],
        ),
    ]
