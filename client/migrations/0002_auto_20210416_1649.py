# Generated by Django 3.0.14 on 2021-04-16 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Name of company'),
        ),
    ]