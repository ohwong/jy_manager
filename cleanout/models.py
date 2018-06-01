from django.db import models
from django.contrib.auth.models import User
from aircraft.models import Aircraft


class AirCraftCleanOut(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "飞机外表清洗"

    aircraft = models.ForeignKey(Aircraft, verbose_name="机号")
    aircraft_type = models.CharField(max_length=32, verbose_name="机型")
    cleanout_date = models.DateField(verbose_name="清洗日期")
    cleanout_user = models.ForeignKey(User, verbose_name="创建者")
    cleanout_department = models.CharField(max_length=32, verbose_name="清洗部门")
    cleanout_method = models.CharField(max_length=192, verbose_name="清洗方式")
    cleanout_status = models.CharField(max_length=32, verbose_name="清洗效果")
    next_clieanout_date = models.DateField(verbose_name="下次计划时间")
    note = models.TextField(blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.aircraft
