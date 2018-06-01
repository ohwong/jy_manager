from datetime import date, timedelta, datetime
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from datastream.models import DataStream
from refused_order.models import RefusedOrder
from mcc.models import MCC
from cleanout.models import AirCraftCleanOut
from observation.models import Observation
from event_handover.models import HandEvent
from aircraft.models import Aircraft


class Command(BaseCommand):

    help = '将本地记录统计更新到数据库'

    def update_aircraft_code(self, code, aircraft):
        for model in self.models:
            model.objects.filter(aircraft__aircraft_code=code).update(aircraft=aircraft)

    @property
    def models(self):
        return [DataStream, RefusedOrder, MCC, AirCraftCleanOut, Observation, HandEvent]

    def delete_repeat_code(self, aircraft):
        objects = Aircraft.objects.filter(aircraft_code=aircraft.aircraft_code).excude(pk=aircraft.pk)
        for obj in objects:
            for model in self.models:
                if model.objects.filter(aircraft=obj):
                    print("delete_error", obj.pk)
                    print("！" * 10)
                    return
            obj.delete()

    def handle(self, *args, **options):
        """"""
        unique_code_list = [x[0] for x in Aircraft.objects.all().values_list("aircraft_code")]
        for code in unique_code_list:
            aircraft = Aircraft.objects.filter(aircraft_code=code).first()
            self.update_aircraft_code(code, aircraft)
