from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Observation(models.Model):
    """观察件"""
    class Meta:
        verbose_name = verbose_name_plural = "观察件记录"

    name = models.CharField(max_length=64, verbose_name="名称")
    aircraft_code = models.CharField(max_length=32, verbose_name="机号")
    item_code = models.CharField(max_length=32, verbose_name="件号")
    sort_code = models.CharField(max_length=32, verbose_name="序号")
    tear_data = models.DateTimeField(verbose_name="拆下日期")
    work_user = models.ForeignKey(User, verbose_name="工作者")
    observation_days = models.IntegerField(verbose_name="拆件天数")
    estimated_closing_date = models.DateTimeField(verbose_name="预计关闭日期", blank=True, null=True)
    closed_date = models.DateTimeField(verbose_name="实际关闭日期", blank=True, null=True)
    closed_user = models.ForeignKey(User, verbose_name="关闭者",
                                    related_name="closed_user", blank=True, null=True)
    tear_reason = RichTextField(verbose_name="拆件原因", blank=True, null=True)
    observation_result = RichTextField(verbose_name="观察结果", blank=True, null=True)

    def __str__(self):
        return self.name
