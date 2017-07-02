from django.db import models
from django.contrib.auth.models import User


class MissionType(models.Model):
    """任务分类"""
    class Meta:
        verbose_name = verbose_name_plural = "任务分类"

    name = models.CharField(verbose_name="名称", max_length=32)

    def __str__(self):
        return self.name


class Mission(models.Model):
    """任务"""
    class Meta:
        verbose_name = verbose_name_plural = "任务"

    title = models.CharField(max_length=191, verbose_name="标题")
    mission_type = models.ForeignKey(MissionType, verbose_name="分类")
    description = models.TextField(verbose_name="描述", blank=True, null=True)
    start_date = models.DateField(verbose_name="开始时间")
    end_date = models.DateField(verbose_name="结束时间")
    created_user = models.ForeignKey(User, related_name="created_user",  verbose_name="创建着")
    mission_user = models.ForeignKey(User, related_name="mission_user", verbose_name="任务派分给")
    created_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    status = models.IntegerField(verbose_name="完成", choices=((0, "未完成"), (1, "已完成")), default=0)

    def __str__(self):
        return self.title


class ThisMonthMission(Mission):
    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = "当月任务"


class MyMonthMission(Mission):
    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = "我的任务"