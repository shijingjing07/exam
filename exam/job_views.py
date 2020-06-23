import time
import base64

from django.shortcuts import render
from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request


# Create your views here.
def fast_execute_sql(request):
    bk_biz_id = request.POST.get('bk_biz_id', 8)
    ip_list = request.POST.getlist('ips', [])

    bk_biz_id = int(bk_biz_id)

    client = get_client_by_request(request)
    params = {
        'bk_biz_id': bk_biz_id
    }
    account_result = client.job.get_own_db_account_list(params)
    db_account_id = account_result['data'][0]['db_account_id']

    script_content = 'show databases;'
    params = {
        'bk_biz_id': bk_biz_id,
        'script_content': str(base64.b64encode(script_content.encode("utf-8")), "utf-8"),
        'db_account_id': db_account_id,
        'ip_list': []
    }
    if ip_list:
        for ip in ip_list:
            params['ip_list'].append({
                'bk_cloud_id': 0,
                'ip': ip
            })
    result = get_client_by_request(request).job.fast_execute_sql(params)
    return JsonResponse({'result': True, 'data': result})


def fast_push_file(request):
    bk_biz_id = request.POST.get('bk_biz_id', 8)

    bk_biz_id = int(bk_biz_id)

    client = get_client_by_request(request)
    params = {
        "bk_biz_id": bk_biz_id,
        "file_target_path": "/tmp/",
        "file_source": [
            {
                "files": [
                    "/root/add_wlist.sh"
                ],
                "account": "root",
                "ip_list": [{
                    'bk_cloud_id': 0,
                    'ip': '172.25.0.20'
                }]
            }
        ],
        "account": "root",
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": "172.25.0.20"
            },
            {
                "bk_cloud_id": 0,
                "ip": "172.25.0.7"
            }
        ]
    }
    result = client.job.fast_push_file(params)
    return JsonResponse({'result': True, 'data': result})
