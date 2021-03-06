from django.db import models


class AircraftManager(models.Manager):
    def valid_name_objects(self):
        return self.filter(show_in_choice=True)

    def name_format_objects(self):
        return self.filter(aircraft_code__regex='(^[a-zA-Z]{1,2}-[0-9]{4}$)|N/A')


class Aircraft(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "机号管理"

    aircraft_code = models.CharField(max_length=32, verbose_name="机号")
    show_in_choice = models.BooleanField(default=True, verbose_name="是否在下拉框中显示")
    objects = AircraftManager()

    def __str__(self):
        return self.aircraft_code
