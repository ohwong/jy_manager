from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from aircraft.models import Aircraft


class HandEvent(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "事件交接"

    AIRCRAFT_TYPE_CHOICES = (
        (1, "737-800"),
        (2, "737-MAX")
    )

    HANDOVER_TYPE_CHOICES = (
        (1, "技术交接"),
        (2, "控制交接")
    )
    STATUS_CHOICES = (
        (0, "closed"),
        (1, "open")
    )

    aircraft_code = models.CharField(max_length=32, verbose_name="机号")
    aircraft = models.ForeignKey(Aircraft)
    aircraft_type = models.IntegerField(verbose_name="机型", choices=AIRCRAFT_TYPE_CHOICES,
                                        default=1)
    subject = models.CharField(max_length=191, verbose_name="主题")
    chapter_code = models.CharField(max_length=64, verbose_name="章节号")
    handover_type = models.IntegerField(choices=HANDOVER_TYPE_CHOICES, verbose_name="交接类型",
                                        default=1)
    publish_user = models.ForeignKey(User, verbose_name="发布人员")
    published_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="状态", default=1)

    def __str__(self):
        return str(self.aircraft_code) + "_" + str(self.aircraft_type)


class Comment(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "事件交接评论"
        ordering = ['-created_at']

    hand_event = models.ForeignKey(HandEvent, verbose_name="事件")
    content = RichTextField(verbose_name="内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    user = models.ForeignKey(User, verbose_name="评论者")

    def __str__(self):
        return str(self.user) + "-" + str(self.hand_event)
