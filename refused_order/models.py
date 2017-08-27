from django.db import models
from django.contrib.auth.models import User


class RefusedOrder(models.Model):
    """退单"""

    class Meta:
        verbose_name = verbose_name_plural = "退单"

    apply_user = models.ForeignKey(User, verbose_name="申请人")
    deal_user = models.ForeignKey(User, related_name='deal_user', verbose_name="处理人",
                                  blank=True, null=True)
    terminal = models.CharField(max_length=32, verbose_name="航站")
    aircraft_code = models.CharField(max_length=64, verbose_name="机号")
    worker_code = models.CharField(max_length=64, verbose_name="工卡号")
    worker_content = models.CharField(max_length=191, verbose_name="工作内容")
    created_at = models.DateField(auto_now_add=True, verbose_name="退单日期")
    has_applied = models.BooleanField(default=False, verbose_name="是否批准")
    note = models.TextField(verbose_name="备注")

    def __str__(self):
        return self.worker_code
