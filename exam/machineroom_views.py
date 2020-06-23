import xlwt
import time
import base64
from io import BytesIO

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator

from blueking.component.shortcuts import get_client_by_request

from exam.models import Host, MachineRoom, Rack


# Create your views here.
def machineroom(request):
    """
    机房
    """
    return render(request, 'exam/machineroom.html')


def search_machinerooms(request):
    name = request.GET.get('name')
    cur_page = request.GET.get('cur_page')
    per_page = request.GET.get('per_page')
    qs = MachineRoom.objects.all()
    if name:
        qs = qs.filter(bk_inst_name__icontains=name)
    paginator = Paginator(qs, per_page)
    page = paginator.page(cur_page)
    data = list()
    for model in page:
        model_dict = model.to_dict()
        rack_count = model.rack_set.count()
        model_dict['rack_count'] = rack_count
        data.append(model_dict)
    return JsonResponse({'result': True, 'data': data, 'total': paginator.count})


def save_machineroom(request):
    id = request.POST.get('id')
    bk_inst_name = request.POST.get('bk_inst_name')
    room_in_use = request.POST.get('room_in_use')
    room_in_use = True if room_in_use == 'true' else False
    if not id:
        machine_room = MachineRoom.objects.create(
            bk_inst_name=bk_inst_name,
            room_in_use=room_in_use
        )
    else:
        machine_room = MachineRoom.objects.get(id=id)
        machine_room.bk_inst_name = bk_inst_name
        machine_room.room_in_use = room_in_use
        machine_room.save()
    data = machine_room.to_dict()
    return JsonResponse({'result': True, 'data': data})


def delete_machineroom(request):
    id = request.POST.get('id')
    machine_room = MachineRoom.objects.get(id=id)
    machine_room.delete()
    return JsonResponse({'result': True})


def rack(request):
    """
    机柜
    :param request:
    :return:
    """
    room_id = request.GET.get('room_id')
    qs = Rack.objects.select_related().filter(machine_room__id=room_id)
    data = list()
    for model in qs:
        model_dict = model.to_dict()
        model_dict['room_name'] = model.machine_room.bk_inst_name
        data.append(model_dict)
    return render(request, 'exam/rack.html', {'rack_list': data})
