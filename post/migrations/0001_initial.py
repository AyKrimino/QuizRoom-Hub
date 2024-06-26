# Generated by Django 5.0.6 on 2024-06-15 20:24

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classroom', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Course id')),
                ('title', models.CharField(max_length=200, verbose_name='Course title')),
                ('content', models.TextField(verbose_name='Course content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Course created at')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Course updated at')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='classroom.classroom', verbose_name='Classroom')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Comment id')),
                ('content', models.TextField(verbose_name='Comment content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Comment created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Comment updated at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='post.coursepost', verbose_name='Course post')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ('-created_at',),
            },
        ),
    ]
