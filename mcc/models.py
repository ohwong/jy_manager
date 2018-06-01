from django.db import models
from django.contrib.auth.models import User
from aircraft.models import Aircraft

# Create your models here.


class MCC(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "MCC指令"

    # 基本信息
    order = models.CharField(max_length=32, verbose_name='工作指令')
    aircraft_code = models.CharField(max_length=32, verbose_name="机号")
    aircraft = models.ForeignKey(Aircraft, verbose_name="机号")
    terminal = models.CharField(max_length=32, verbose_name="航站")
    date = models.DateField(verbose_name="日期")
    discrepancy_or_reason = models.TextField(verbose_name='故障描述或工作原因', blank=True, null=True, default='')
    work_content = models.TextField(verbose_name='工作内容', blank=True, null=True, default='')

    plan_nam_hours = models.CharField(max_length=32, verbose_name="计划工时", default='', blank=True, null=True)
    is_rll = models.BooleanField(default=True, verbose_name="是否必检")
    is_run_test = models.BooleanField(default=True, verbose_name="是否试车")
    reference = models.CharField(max_length=64, default='', verbose_name="依据文件", blank=True, null=True)
    author = models.ForeignKey(User, verbose_name="编写者", related_name='author')
    verifier = models.ForeignKey(User, verbose_name="审核者", blank=True, null=True, related_name='verifier')

    # 工作反馈
    feedback_content = models.TextField(verbose_name="工作反馈", default='', blank=True, null=True)
    actual_nam_hours = models.CharField(max_length=32, verbose_name="实际工时", default='', blank=True, null=True)
    worker = models.ForeignKey(User, verbose_name="工作者", blank=True, null=True, related_name='worker')
    inspector = models.ForeignKey(User, verbose_name="检验员", blank=True, null=True, related_name='inspector')
    feed_back_date = models.DateField(blank=True, null=True, verbose_name="日期")

    def __str__(self):
        return self.order


class MccEquipment(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "航材与工装设备信"

    # 航材与工装设备信
    mcc = models.ForeignKey(MCC)
    equipment_name = models.CharField(max_length=32, verbose_name="名称", default='', blank=True, null=True)
    equipment_part = models.CharField(max_length=32, verbose_name="件号", default='', blank=True, null=True)
    equipment_quantity = models.IntegerField(verbose_name="数量", blank=True, null=True)
    equipment_remark = models.CharField(max_length=32, verbose_name="备注", default='', blank=True, null=True)

    def __str__(self):
        return self.equipment_name + ";" + self.equipment_part