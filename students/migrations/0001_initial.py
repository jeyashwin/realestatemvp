# Generated by Django 3.1.2 on 2021-03-11 17:06

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import students.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_remove_userlandlord_profilepicture'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoommatePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=students.models.roompost_image_file_path, verbose_name='Image')),
                ('image1', imagekit.models.fields.ProcessedImageField(upload_to=students.models.roompost_image_file_path, verbose_name='Image')),
                ('image2', imagekit.models.fields.ProcessedImageField(upload_to=students.models.roompost_image_file_path, verbose_name='Image')),
                ('image3', imagekit.models.fields.ProcessedImageField(upload_to=students.models.roompost_image_file_path, verbose_name='Image')),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('heart', models.ManyToManyField(blank=True, related_name='hearts', to='users.UserStudent')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='users.userstudent')),
            ],
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('roomatePost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='students.roommatepost')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentedstudent', to='users.userstudent')),
            ],
            options={
                'ordering': ['createdDate'],
            },
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField()),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentreply', to='students.postcomment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repliedstudent', to='users.userstudent')),
            ],
            options={
                'ordering': ['createdDate'],
            },
        ),
    ]