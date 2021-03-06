# Generated by Django 2.1.8 on 2020-06-19 11:24

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_host_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineRoom',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='唯一标识')),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('creator', models.CharField(blank=True, max_length=64, null=True, verbose_name='创建人')),
                ('modifier', models.CharField(blank=True, max_length=64, null=True, verbose_name='更新人')),
                ('bk_inst_name', models.CharField(max_length=64, verbose_name='名称')),
                ('room_in_use', models.BooleanField(default=False, verbose_name='使用标识')),
            ],
            options={
                'verbose_name': '机房',
                'db_table': 'machine_room',
            },
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='唯一标识')),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('creator', models.CharField(blank=True, max_length=64, null=True, verbose_name='创建人')),
                ('modifier', models.CharField(blank=True, max_length=64, null=True, verbose_name='更新人')),
                ('bk_inst_name', models.CharField(max_length=64, verbose_name='名称')),
                ('machine_room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exam.MachineRoom', verbose_name='机房')),
            ],
            options={
                'verbose_name': '机柜',
                'db_table': 'rack',
            },
        ),
    ]
