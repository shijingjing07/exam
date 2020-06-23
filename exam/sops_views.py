import time
import base64

from django.shortcuts import render
from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request


# Create your views here.
def create_task(request):
    bk_biz_id = request.POST.get('bk_biz_id', 4)
    template_id = request.POST.get('template_id', 2)
    name = request.POST.get('name')
    sleep_time = request.POST.get('sleep_time')

    bk_biz_id = int(bk_biz_id)
    template_id = int(template_id)
    sleep_time = int(sleep_time)

    params = {
        "bk_biz_id": bk_biz_id,
        "template_id": template_id,
        "name": name,
        "constants": {
            "${sleep_time}": sleep_time
        }
    }
    client = get_client_by_request(request)
    result = client.sops.create_task(params)
    task_id = result['data']['task_id']
    print(task_id)
    return JsonResponse({'result': True, 'data': task_id})


def operate_task(request):
    bk_biz_id = request.POST.get('bk_biz_id', 4)
    task_id = request.POST.get('task_id')
    action = request.POST.get('action')

    bk_biz_id = int(bk_biz_id)

    params = {
        "action": action,
        "bk_biz_id": bk_biz_id,
        "task_id": task_id
    }
    client = get_client_by_request(request)
    result = client.sops.operate_task(params)
    return JsonResponse({'result': True})


def task_status(request):
    bk_biz_id = request.POST.get('bk_biz_id', 4)
    task_id = request.POST.get('task_id')

    bk_biz_id = int(bk_biz_id)

    params = {
        "bk_biz_id": bk_biz_id,
        "task_id": task_id
    }
    client = get_client_by_request(request)
    result = client.sops.get_task_status(params)
    return JsonResponse({'result': True, 'data': result})


def task_detail(request):
    bk_biz_id = request.POST.get('bk_biz_id', 4)
    task_id = request.POST.get('task_id')

    bk_biz_id = int(bk_biz_id)

    params = {
        "bk_biz_id": bk_biz_id,
        "task_id": task_id
    }
    client = get_client_by_request(request)
    result = client.sops.get_task_detail(params)
    return JsonResponse({'result': True, 'data': result})


