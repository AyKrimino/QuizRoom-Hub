# Generated by Django 5.0.6 on 2024-06-15 20:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Student id')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Bio')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/', verbose_name='Profile Picture')),
            ],
            options={
                'verbose_name': 'Student Profile',
                'verbose_name_plural': 'Student Profiles',
                'ordering': ('date_of_birth',),
            },
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Teacher id')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Bio')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/', verbose_name='Profile Picture')),
                ('years_of_experience', models.PositiveIntegerField(blank=True, null=True, verbose_name='Years of Experience')),
            ],
            options={
                'verbose_name': 'Teacher Profile',
                'verbose_name_plural': 'Teacher Profiles',
                'ordering': ('-years_of_experience', 'date_of_birth'),
            },
        ),
    ]
