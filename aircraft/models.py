from django.db import models


class Aircraft(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "机号管理"

    aircraft_code = models.CharField(max_length=32, verbose_name="机号")

    def __str__(self):
        return self.aircraft_code
