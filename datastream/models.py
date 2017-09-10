from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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
        (1, "飞机BAT电门置于ON位到飞机最后一个舱门关闭"),
        (2, "飞机最后一个舱门关闭到飞机启动双发（发动机慢车功率，后缘襟翼放下5度）"),
        (3, "双发启动后到双发达到起飞功率（飞机在地面，处于起飞构型）"),
        (4, "双发达到起飞功率到空速≧130节"),
        (5, "空速≧130节到飞机离地"),
        (6, "飞机离地到高度1500英尺（发动机起飞功率，襟翼≦5度）"),
        (7, "高度1500英尺（发动机起飞功率）到高度1500英尺（发动机非起飞功率且襟翼>25度）"),
        (8, "高度1500英尺到机轮着地 "),
        (9, "机轮着地到空速≦80节（飞机在地面，发动机反推工作，扰流板工作）"),
        (10, "空速≦80节到双发关车"),
    )

    FAULT_TYPE_CHOICES = (
        (1, "一般"),
        (2, "突发"),
        (3, "重复"),
        (4, "疑难"),
        (5, "重大"),
    )

    TEMPERATURE_CHOICE = (
        ("28度以上", "28度以上"),
        ("10-28度", "10-28度"),
        ("10度以下", "10度以下")
    )

    STATUS_CHOICES = (
        (0, "closed"),
        (1, "open")
    )

    class Meta:
        verbose_name = verbose_name_plural = "数据录入"

    the_year = models.IntegerField(verbose_name="年", default=timezone.now().year)
    the_month = models.IntegerField(verbose_name="月", default=timezone.now().month)
    the_day = models.IntegerField(verbose_name="日", default=timezone.now().day)
    aircraft_code = models.CharField(max_length=32, verbose_name="机号")
    flight_type = models.CharField(max_length=32, verbose_name="航班号")
    location = models.CharField(max_length=64, verbose_name="地点")
    weather = models.CharField(max_length=64, verbose_name="天气")
    temperature = models.CharField(max_length=64, verbose_name="温度",
                                   choices=TEMPERATURE_CHOICE)
    fault_phase = models.IntegerField(verbose_name="故障阶段", choices=FAULT_PHASE_CHOICES,
                                      default=1)

    fault_description = RichTextField(verbose_name="故障描述", blank=True, null=True)
    fault_type = models.IntegerField(choices=FAULT_TYPE_CHOICES, verbose_name="故障类型", default=1)
    chapter = models.CharField(max_length=64, verbose_name="章", blank=True, null=True)
    knob = models.CharField(max_length=64, verbose_name="节", blank=True, null=True)
    deal_method = RichTextField(verbose_name="处理措施", blank=True, null=True)
    after_deal_method = RichTextField(verbose_name="后续处理措施", blank=True, null=True)
    record_paper_code = models.CharField(max_length=64, verbose_name="记录纸号", blank=True, null=True)
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
    # 延误时间应客户要求改为Ｃhar类型
    delay_time = models.CharField(verbose_name="延误时间", blank=True, null=True, max_length=64)
    has_delayed = models.IntegerField(default=0, choices=YES_OR_NO, verbose_name="是否延误")
    is_sdr = models.IntegerField(verbose_name="是否SDR", default=0, choices=YES_OR_NO)
    unexpected_stay_day = models.IntegerField(verbose_name="非计划停场天数", default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="录入时间")

    create_user = models.ForeignKey(User, verbose_name="录入人员")
    has_checked = models.BooleanField(verbose_name="完成审核?", default=False)
    check_user = models.ForeignKey(User, related_name="check_user",
                                   verbose_name="审核人员", blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="状态", default=1)

    def __str__(self):
        return str(self.aircraft_code) + "-" + str(self.flight_type) + "-" +\
               dict(self.FAULT_PHASE_CHOICES).get(self.fault_phase)
