# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from . import host_views
from . import machineroom_views
from . import process_views
from . import job_views
from . import sops_views

urlpatterns = (
    # 主机查询
    url(r'^$', host_views.home),
    url(r'^getHosts/$', host_views.get_hosts),
    url(r'^searchDepartmentUser/$', host_views.search_department_user),
    url(r'^hostBindOwner/$', host_views.host_bind_owner),
    url(r'^hostUnbindOwner/$', host_views.host_unbind_owner),
    url(r'^hostExport/$', host_views.host_export),
    url(r'^syncHosts/$', host_views.sync_hosts),

    # 机房管理
    url(r'^machineroom$', machineroom_views.machineroom),
    url(r'^searchMachineRooms/$', machineroom_views.search_machinerooms),
    url(r'^saveMachineRoom/$', machineroom_views.save_machineroom),
    url(r'^deleteMachineRoom/$', machineroom_views.delete_machineroom),
    url(r'^rack/$', machineroom_views.rack),

    # 进程查询
    url(r'^process$', process_views.process),
    url(r'^bizTopo/$', process_views.get_biz_topo),
    url(r'^searchHosts/$', process_views.search_hosts),
    url(r'^searchProcess/$', process_views.search_process_info),
    url(r'^processDetail/$', process_views.process_detail),

    # 作业测试
    url(r'^executeSql/$', job_views.fast_execute_sql),
    url(r'^pushFile/$', job_views.fast_push_file),

    # 标准运维测试
    url(r'^createTask/$', sops_views.create_task),
    url(r'^operateTask/$', sops_views.operate_task),
    url(r'^taskStatus/$', sops_views.task_status),
    url(r'^taskDetail/$', sops_views.task_detail),
    # 其他
    url(r'^testApi/$', views.test_api),
)

