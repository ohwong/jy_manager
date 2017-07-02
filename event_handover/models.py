from django.db import models
from django.contrib.auth.models import User


class HandEvent(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "事件交接"

    STATUS_CHOICES = (
        (0, "closed"),
        (1, "open")
    )

    aircraft_code = models.CharField(max_length=32, verbose_name="机号")
    aircraft_type = models.CharField(max_length=32, verbose_name="机型")
    subject = models.CharField(max_length=191, verbose_name="主题")
    chapter_code = models.CharField(max_length=64, verbose_name="章节号")
    handover_type = models.CharField(max_length=64, verbose_name="交接类型")
    publish_user = models.ForeignKey(User, verbose_name="发布人员")
    published_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="状态", default=1)

    def __str__(self):
        return str(self.aircraft_code) + "_" + str(self.aircraft_type)


class Comment(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "事件交接评论"

    hand_event = models.ForeignKey(HandEvent, verbose_name="事件")
    content = models.TextField(verbose_name="内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    user = models.ForeignKey(User, verbose_name="评论者")

    def __str__(self):
        return str(self.user) + "-" + str(self.hand_event)
