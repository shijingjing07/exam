import uuid
from datetime import datetime

from django.db import models
from django.db.models.fields import DateTimeField, DecimalField
from django.db.models.fields.related import ManyToManyField


# Create your models here.
class BaseModel(models.Model):
    id = models.CharField(verbose_name=u'唯一标识', primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    created = models.DateTimeField(verbose_name=u'创建时间', default=datetime.now, blank=True)
    updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True, blank=True)
    creator = models.CharField(verbose_name=u'创建人', max_length=64, blank=True, null=True)
    modifier = models.CharField(verbose_name=u'更新人', max_length=64, blank=True, null=True)

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                value = [i.id for i in value] if self.pk else None
            if isinstance(f, DecimalField):
                value = float(value)
            if isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
            data[f.name] = value
        return data

    class Meta:
        abstract = True


class Host(BaseModel):
    bk_biz_id = models.IntegerField(verbose_name=u'业务ID', null=False, blank=False)
    bk_biz_name = models.CharField(verbose_name=u'业务名称', null=False, blank=False, max_length=64)
    bk_host_id = models.IntegerField(verbose_name=u'主机ID', null=False, blank=False)
    bk_host_name = models.CharField(verbose_name=u'主机名称', null=False, blank=False, max_length=64)
    bk_host_innerip = models.CharField(verbose_name=u'主机IP', null=True, blank=True, max_length=64)
    owner = models.CharField(verbose_name=u'属主', null=True, blank=True, max_length=64)

    class Meta:
        verbose_name = u'主机'
        db_table = 'host'


class MachineRoom(BaseModel):
    bk_inst_name = models.CharField(verbose_name=u'名称', null=False, blank=False, max_length=64)
    room_in_use = models.BooleanField(verbose_name=u'使用标识', default=False)

    class Meta:
        verbose_name = u'机房'
        db_table = 'machine_room'


class Rack(BaseModel):
    bk_inst_name = models.CharField(verbose_name=u'名称', null=False, blank=False, max_length=64)
    machine_room = models.ForeignKey(MachineRoom, verbose_name=u'机房',
                                     null=False, blank=False, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = u'机柜'
        db_table = 'rack'
