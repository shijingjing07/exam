# Generated by Django 2.1.8 on 2020-06-17 16:19

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='唯一标识')),
                ('delflag', models.BooleanField(default=False, verbose_name='删除标识')),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('creator', models.CharField(blank=True, max_length=64, null=True, verbose_name='创建人')),
                ('modifier', models.CharField(blank=True, max_length=64, null=True, verbose_name='更新人')),
                ('bk_biz_id', models.IntegerField(verbose_name='业务ID')),
                ('bk_biz_name', models.CharField(max_length=64, verbose_name='业务名称')),
                ('bk_host_id', models.IntegerField(verbose_name='主机ID')),
                ('bk_host_name', models.CharField(max_length=64, verbose_name='主机名称')),
                ('bk_host_innerip', models.CharField(blank=True, max_length=64, null=True, verbose_name='主机IP')),
            ],
            options={
                'verbose_name': '主机',
                'db_table': 'host',
            },
        ),
    ]