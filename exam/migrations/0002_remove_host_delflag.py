# Generated by Django 2.1.8 on 2020-06-17 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='delflag',
        ),
    ]