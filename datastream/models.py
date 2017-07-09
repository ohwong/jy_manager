from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class DataStream(models.Model):
    """数据录入"""
    YES_OR_NO = (
        (0, "否"),
        (1, "是"),
    )
    FAULT_RESULT_CHOICES = (
        (0, "无"),
        (1, "滑回"),
        (2, "备降"),
        (3, "中断"),
        (4, "起飞"),
        (5, "返航")
    )

    FAULT_PHASE_CHOICES = (
        (1, "航前"),
        (2, "过站"),
        (3, "航后"),
        (4, "推出启动"),
        (5, "滑行"),
        (6, "起飞"),
        (7, "爬升"),
        (8, "巡航"),
        (9, "下降"),
        (10, "进近"),
        (11, "落地滑跑"),
    )

    class Meta:
        verbose_name = verbose_name_plural = "数据录入"

    the_date = models.DateField(verbose_name="日期")
    aircraft_code = models.CharField(max_length=32, verbose_name="机号")
    flight_type = models.CharField(max_length=32, verbose_name="航班号")
    location = models.CharField(max_length=64, verbose_name="地点")
    weather = models.CharField(max_length=64, verbose_name="天气")
    temperature = models.CharField(max_length=64, verbose_name="温度")
    fault_phase = models.IntegerField(verbose_name="故障阶段", choices=FAULT_PHASE_CHOICES,
                                      default=1)

    fault_description = RichTextField(verbose_name="故障描述")
    fault_type = models.CharField(max_length=64, verbose_name="故障类型")
    chapter = models.CharField(max_length=64, verbose_name="章")
    knob = models.CharField(max_length=64, verbose_name="节")
    deal_method = RichTextField(verbose_name="处理措施")
    record_paper_code = models.CharField(max_length=64, verbose_name="记录纸号")
    mel_or_cdl_file = models.CharField(max_length=64, verbose_name="MEL/CDL依据文件",
                                       blank=True, null=True)
    parts_name = models.CharField(max_length=64, verbose_name="拆换件名称",
                                  blank=True, null=True)
    strike_parts_code = models.CharField(max_length=64, verbose_name="拆下件号",
                                         blank=True, null=True)
    strike_parts_num = models.CharField(max_length=64, verbose_name="拆下序号",
                                        blank=True, null=True)

    mount_parts_code = models.CharField(max_length=64, verbose_name="装上件号",
                                        blank=True, null=True)
    mount_parts_num = models.CharField(max_length=64, verbose_name="装上序号",
                                       blank=True, null=True)
    mount_date = models.DateTimeField(verbose_name="装机时间", blank=True, null=True)
    fault_result = models.IntegerField(verbose_name="故障后果", choices=FAULT_RESULT_CHOICES,
                                       default=0)
    delay_reason = models.TextField(verbose_name="延误原因", blank=True, null=True)
    delay_time = models.DateTimeField(verbose_name="延误时间", blank=True, null=True)
    has_delayed = models.IntegerField(default=0, choices=YES_OR_NO, verbose_name="是否延误")
    is_sdr = models.IntegerField(verbose_name="是否SDR", default=0, choices=YES_OR_NO)
    unexpected_stay_day = models.IntegerField(verbose_name="非计划停场天数", default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="录入时间")

    create_user = models.ForeignKey(User, verbose_name="录入人员")
    has_checked = models.BooleanField(verbose_name="完成审核?", default=False)
    check_user = models.ForeignKey(User,related_name="check_user",
                                   verbose_name="审核人员", blank=True, null=True)

    def __str__(self):
        return self.fault_type
