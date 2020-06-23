import xlwt
from io import BytesIO
import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator

from blueking.component.shortcuts import get_client_by_request

from exam.models import Host

# Create your views here.


def home(request):
    """
    首页
    """
    result = get_client_by_request(request).cc.search_business()
    biz_list = result['data']['info']
    # 部门
    params = {
        'no_page': True
    }
    result = get_client_by_request(request).usermanage.list_departments(params)
    dept_list = result['data']
    return render(request, 'exam/host.html', {'biz_list': biz_list, 'dept_list': dept_list})


def search_department_user(request):
    dept_id = request.GET.get('dept_id')
    client = get_client_by_request(request)
    params = {
        'id': int(dept_id),
        'no_page': True
    }
    result = client.usermanage.list_department_profiles(params)
    return JsonResponse({'result': True, 'data': result['data']})


def host_bind_owner(request):
    """
    绑定属主
    :param request:
    :return:
    """
    owner = request.POST.get('owner')
    host_ids = request.POST.get('host_ids')
    client = get_client_by_request(request)
    params = {
        "bk_supplier_account": "0",
        "bk_host_id": host_ids,
        "data": {
            "owner": owner
        }
    }
    result = client.cc.update_host(params)
    host_id_list = host_ids.split(',')
    Host.objects.filter(bk_host_id__in=host_id_list).update(owner=owner)
    return JsonResponse({'result': True})


def host_unbind_owner(request):
    """
    解绑属主
    :param request:
    :return:
    """
    host_ids = request.POST.get('host_ids')
    client = get_client_by_request(request)
    params = {
        "bk_supplier_account": "0",
        "bk_host_id": host_ids,
        "data": {
            "owner": ""
        }
    }
    result = client.cc.update_host(params)
    host_id_list = host_ids.split(',')
    Host.objects.filter(bk_host_id__in=host_id_list).update(owner="")
    return JsonResponse({'result': True})


def host_export(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    owner = request.GET.get('owner')

    qs = Host.objects.all()
    if bk_biz_id:
        qs = qs.filter(bk_biz_id=bk_biz_id)
    if owner:
        qs = qs.filter(owner=owner)

    ws = xlwt.Workbook()
    sheet = ws.add_sheet(u'主机列表')
    sheet.write(0, 0, '业务ID')
    sheet.write(0, 1, '业务名称')
    sheet.write(0, 2, '主机名')
    sheet.write(0, 3, '内网IP')
    sheet.write(0, 4, '属主')

    row_index = 1
    for model in qs:
        sheet.write(row_index, 0, model.bk_biz_id)
        sheet.write(row_index, 1, model.bk_biz_name)
        sheet.write(row_index, 2, model.bk_host_name)
        sheet.write(row_index, 3, model.bk_host_innerip)
        sheet.write(row_index, 4, model.owner)
        row_index += 1

    sio = BytesIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename=hosts.xls"
    response.write(sio.getvalue())
    return response


def get_hosts(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    owner = request.GET.get('owner')
    create_time = request.GET.get('create_time')
    cur_page = request.GET.get('cur_page')
    per_page = request.GET.get('per_page')
    qs = Host.objects.all()
    if bk_biz_id:
        qs = qs.filter(bk_biz_id=bk_biz_id)
    if owner:
        qs = qs.filter(owner__icontains=owner)
    if create_time:
        start_time = create_time.split('-')[0]
        end_time = create_time.split('-')[1]
        start_time = datetime.datetime.strptime(start_time.strip(), '%Y/%m/%d')
        end_time = datetime.datetime.strptime(end_time.strip(), '%Y/%m/%d')
        qs = qs.filter(created__range=(start_time, end_time))
    paginator = Paginator(qs, per_page)
    page = paginator.page(cur_page)
    data = list()
    for model in page:
        data.append(model.to_dict())
    return JsonResponse({'result': True, 'data': data, 'total': paginator.count})


def sync_hosts(request):
    from .celery_tasks import sync_hosts
    sync_hosts()
    return JsonResponse({'result': True})
