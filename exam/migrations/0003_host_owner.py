# Generated by Django 2.1.8 on 2020-06-17 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_remove_host_delflag'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='owner',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='属主'),
        ),
    ]