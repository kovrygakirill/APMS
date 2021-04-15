# Generated by Django 3.0.14 on 2021-04-15 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название проекта')),
                ('description', models.TextField()),
                ('start_date', models.DateField(verbose_name='Начало проекта')),
                ('release_date', models.DateField(verbose_name='Конец проекта')),
                ('status', models.CharField(choices=[('p', 'Planned'), ('i', 'In_progress'), ('t', 'Testing'), ('r', 'Release')], max_length=1)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='client.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название задачи')),
                ('description', models.TextField()),
                ('start_datetime', models.DateTimeField(verbose_name='Начало выполнения задачи')),
                ('release_datetime', models.DateTimeField(verbose_name='Конец выполнения задачи')),
                ('total_time', models.FloatField(verbose_name='Общее время выполнения задачи в часах')),
                ('type', models.CharField(choices=[('p', 'Programming'), ('y', 'Deploy'), ('t', 'Testing'), ('d', 'Design'), ('l', 'Layout')], max_length=1)),
                ('status', models.CharField(choices=[('t', 'To_do'), ('i', 'In_progress'), ('t', 'Testing'), ('d', 'Done')], max_length=1)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='project.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to=settings.AUTH_USER_MODEL, verbose_name='Кто выполняет задачу')),
            ],
        ),
        migrations.CreateModel(
            name='CommentTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('comment', models.TextField()),
                ('status', models.CharField(choices=[('t', 'To_do'), ('i', 'In_progress'), ('t', 'Testing'), ('d', 'Done')], max_length=1)),
                ('time', models.FloatField(verbose_name='Время выполнения задачи в часах')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_task', to='project.Task')),
            ],
        ),
    ]
