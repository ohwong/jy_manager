from django.db import models
from django.contrib.auth.models import User


class DataStream(models.Model):
    """数据录入"""

    class Meta:
        verbose_name = verbose_name_plural = "数据录入"

    the_date = models.DateField(verbose_name="日期")
    aircraft_code = models.CharField(max_length=32, verbose_name="机号")
    flight_type = models.CharField(max_length=32, verbose_name="航班号")
    location = models.CharField(max_length=64, verbose_name="地点")
    weather = models.CharField(max_length=64, verbose_name="天气")
    temperature = models.CharField(max_length=64, verbose_name="温度")
    fault_time = models.CharField(max_length=191, verbose_name="故障时段")
    fault_phase = models.CharField(max_length=191, verbose_name="故障阶段")

    fault_description = models.TextField(verbose_name="故障描述")
    fault_type = models.CharField(max_length=64, verbose_name="故障类型")
    chapter = models.CharField(max_length=64, verbose_name="章")
    knob = models.CharField(max_length=64, verbose_name="节")
    deal_method = models.TextField(verbose_name="处理措施")
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
    fault_result = models.TextField(verbose_name="故障后果", blank=True, null=True)
    delay_property = models.CharField(verbose_name="延误性质", max_length=191,
                                      blank=True, null=True)
    delay_reason = models.TextField(verbose_name="延误原因", blank=True, null=True)
    delay_time = models.DateTimeField(verbose_name="延误时间", blank=True, null=True)
    is_sdr = models.BooleanField(verbose_name="是否SDR", default=False)
    unexpected_stay_day = models.IntegerField(verbose_name="非计划停场天数", default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="录入时间")

    create_user = models.ForeignKey(User, verbose_name="录入人员")
    has_checked = models.BooleanField(verbose_name="完成审核?", default=False)
    check_user = models.ForeignKey(User,related_name="check_user",
                                   verbose_name="审核人员", blank=True, null=True)

    def __str__(self):
        return self.fault_type
