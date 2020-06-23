# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import math

from celery.schedules import crontab
from celery.task import periodic_task

from blueking.component.shortcuts import get_client_by_user
from blueapps.utils.logger import logger_celery

from .models import Host


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def sync_hosts():
    logger_celery.debug('sync hosts begin')
    client = get_client_by_user('admin')
    # 主机数量
    hosts = client.cc.search_host({'page': {'start': 0, 'limit': 1}})
    count = hosts['data']['count']
    # 每页数量
    per_page = 10
    # 页数
    page_number = math.ceil(count / per_page)

    for i in range(page_number):
        hosts = client.cc.search_host(query_host_params(i * per_page, per_page))
        for host_data in hosts['data']['info']:
            qs = Host.objects.filter(bk_host_id=host_data['host']['bk_host_id'])
            if qs.exists():
                host = qs.first()
            else:
                host = Host()
            if host_data['biz']:
                host.bk_biz_id = host_data['biz'][0]['bk_biz_id']
                host.bk_biz_name = host_data['biz'][0]['bk_biz_name']
                host.bk_host_id = host_data['host']['bk_host_id']
                host.bk_host_name = host_data['host']['bk_host_name']
                host.bk_host_innerip = host_data['host']['bk_host_innerip']
                host.owner = host_data['host']['operator']
                host.save()
    logger_celery.debug('sync hosts end')


def query_host_params(start, limit):
    params = {
        "condition": [
            {
                "bk_obj_id": "host",
                "fields": [],
                "condition": []
            },
            {
                "bk_obj_id": "module",
                "fields": [],
                "condition": []
            },
            {
                "bk_obj_id": "set",
                "fields": [],
                "condition": []
            },
            {
                "bk_obj_id": "biz",
                "fields": [],
                "condition": []
            }
        ],
        "page": {
            "start": start,
            "limit": limit,
            "sort": "bk_host_id"
        }
    }
    return params
