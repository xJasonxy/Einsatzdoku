# Generated by Django 2.2.6 on 2019-12-19 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doku', '0011_auto_20191116_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lagekarte',
            name='Temp',
        ),
        migrations.AddField(
            model_name='lagekarte',
            name='Data',
            field=models.TextField(default=''),
        ),
    ]