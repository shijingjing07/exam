import time
import base64

from django.shortcuts import render
from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request

# Create your views here.


def process(request):
    result = get_client_by_request(request).cc.search_business()
    biz_list = result['data']['info']
    return render(request, 'exam/process.html', {'biz_list': biz_list})


def get_biz_topo(request):
    """
    获取业务拓扑树
    """
    biz_id = request.GET.get('bk_biz_id', 2)
    result = get_client_by_request(request).cc.search_biz_inst_topo({'bk_biz_id': int(biz_id)})
    import json
    data = json.dumps(result['data'])
    print(data)
    if result['result']:
        return JsonResponse({'result': True, 'data': get_topo_sub(result['data'])})
    else:
        return JsonResponse({'result': False, 'message': result['message']})


def get_topo_sub(data):
    res = []
    for child in data:
        obj = dict()
        obj['id'] = str(child['bk_inst_id'])+'_'+str(child['bk_obj_id'])
        obj['text'] = child['bk_inst_name']
        if child['child']:
            obj['children'] = get_topo_sub(child['child'])
        res.append(obj)
    return res


def search_hosts(request):
    bk_biz_id = request.POST.get('bk_biz_id', 8)
    bk_set_ids = request.POST.getlist('bk_set_ids[]')
    bk_module_ids = request.POST.getlist('bk_module_ids[]')

    bk_biz_id = int(bk_biz_id)
    bk_set_ids = [int(bk_set_id) for bk_set_id in bk_set_ids]
    bk_module_ids = [int(bk_module_id) for bk_module_id in bk_module_ids]

    client = get_client_by_request(request)
    result = client.cc.search_host(query_host_params(bk_biz_id, bk_set_ids, bk_module_ids))
    import json
    data = json.dumps(result)
    print(data)
    return JsonResponse({'result': True, 'data': result['data']['info']})


def search_process_info(request):
    bk_biz_id = request.GET.get('bk_biz_id', 8)
    script_params = request.GET.get('script_params')
    ip_list = request.GET.getlist('ips[]')

    bk_biz_id = int(bk_biz_id)

    script_content = '#!/bin/bash\n ps aux | grep $1 | grep -v grep'

    client = get_client_by_request(request)
    exec_result = fast_script_exec(client, bk_biz_id, script_content, script_params, ip_list)
    result = sync_fetch_job_result(client, bk_biz_id, exec_result['data']['job_instance_id'])
    return JsonResponse({'result': True, 'data': result})


def fast_script_exec(client, bk_biz_id, script_content, script_param, ip_list):
    script_content = str(base64.b64encode(script_content.encode("utf-8")), "utf-8")
    script_param = str(base64.b64encode(script_param.encode("utf-8")), "utf-8")
    params = {
        'bk_biz_id': bk_biz_id,
        'script_content': script_content,
        'script_param': script_param,
        'script_type': 1,
        'account': 'root'
    }
    if ip_list:
        params['ip_list'] = list()
        for ip in ip_list:
            if ip:
                params['ip_list'].append({
                    'bk_cloud_id': 0,
                    'ip': ip
                })
    result = client.job.fast_execute_script(params)
    return result


def sync_fetch_job_result(client, bk_biz_id, job_instance_id, type=None):
    result = []
    if job_instance_id:
        while True:
            params = {
                'bk_biz_id': bk_biz_id,
                'job_instance_id': job_instance_id
            }
            status_result = client.job.get_job_instance_status(params)
            if status_result['data']['is_finished']:
                log_result = client.job.get_job_instance_log(params)
                if not type:
                    ip_logs = log_result['data'][0]['step_results'][0]['ip_logs']
                    for ip_log in ip_logs:
                        ip = ip_log['ip']
                        process_count = len(ip_log['log_content'].split('\n')) if ip_log['log_content'] else 0
                        result.append({
                            'bk_biz_id': bk_biz_id,
                            'ip': ip,
                            'process_count': process_count
                        })
                else:
                    process_dict = dict()
                    ip_log = log_result['data'][0]['step_results'][0]['ip_logs'][0]
                    process_list = ip_log['log_content'].split('\n')
                    for process_info in process_list:
                        if process_info:
                            fs = process_info.split()
                            record_dict = dict()
                            record_dict['UID'] = fs[0]
                            record_dict['PID'] = fs[1]
                            record_dict['PPID'] = fs[2]
                            record_dict['TIME'] = fs[6]
                            record_dict['CMD'] = fs[7]
                            record_dict['PORT'] = '--'
                            process_dict[fs[1]] = record_dict
                            result.append(record_dict)
                    ip_log2 = log_result['data'][1]['step_results'][0]['ip_logs'][0]
                    port_list = ip_log2['log_content'].split('\n')
                    for port in port_list:
                        if port:
                            pid = port.split('&gt;')[0]
                            port_log = port.split('&gt;')[1]
                            if port_log != 'failed':
                                process_dict[pid]['PORT'] = port_log.split()[3]
                break
            time.sleep(1)
    return result


def process_detail(request):
    bk_biz_id = request.GET.get('bk_biz_id', 8)
    process_key = request.GET.get('process_key')
    ip = request.GET.get('ip')

    bk_biz_id = int(bk_biz_id)

    client = get_client_by_request(request)

    params = {
        'bk_biz_id': bk_biz_id,
        'bk_job_id': 158
    }
    result = client.job.get_job_detail(params)
    job_steps = result['data']['steps']
    for step in job_steps:
        if ip:
            step['ip_list'] = [{'bk_cloud_id': 0, 'ip': ip}]
        if process_key:
            step['script_param'] = str(base64.b64encode(process_key.encode("utf-8")), "utf-8")

    params['steps'] = job_steps
    execute_result = client.job.execute_job(params)
    result = sync_fetch_job_result(client, bk_biz_id, execute_result['data']['job_instance_id'], type=1)
    return render(request, 'exam/process_detail.html', {'proc_list': result, 'bk_biz_id': bk_biz_id, 'ip': ip})


def query_host_params(bk_biz_id, bk_set_ids, bk_module_ids):
    _params = {
        "condition": [],
        "page": {
            "start": 0,
            "limit": 10,
            "sort": "bk_host_id"
        },
        "pattern": ""
    }

    bk_biz_id_params = {
        "bk_obj_id": "biz",
        "fields": [],
        "condition": []
    }
    if bk_biz_id:
        bk_biz_id_params['condition'].append({
            "field": "bk_biz_id",
            "operator": "$eq",
            "value": bk_biz_id
        })
    _params['condition'].append(bk_biz_id_params)

    bk_set_id_params = {
        "bk_obj_id": "set",
        "fields": [],
        "condition": []
    }
    if bk_set_ids:
        bk_set_id_params['condition'].append({
            "field": "bk_set_id",
            "operator": "$in",
            "value": bk_set_ids
        })
    _params['condition'].append(bk_set_id_params)

    bk_module_id_params = {
        "bk_obj_id": "module",
        "fields": [],
        "condition": []
    }
    if bk_module_ids:
        bk_module_id_params['condition'].append({
            "field": "bk_module_id",
            "operator": "$in",
            "value": bk_module_ids
        })
    _params['condition'].append(bk_module_id_params)
    return _params


