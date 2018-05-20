from datetime import date, timedelta, datetime

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

    def fetch_aircraft_by_model(self, model):
        queryset = model.objects.all().values('aircraft_code').distinct()
        return [x['aircraft_code'] for x in queryset]

    @property
    def models(self):
        return [DataStream, RefusedOrder, MCC, AirCraftCleanOut, Observation, HandEvent]

    def handle(self, *args, **options):
        """"""
        aircraft_codes = list()
        for model in self.models:
            aircraft_codes += self.fetch_aircraft_by_model(model)

        for code in aircraft_codes:
            if code.isdigit():
                code = "B-" + code
            Aircraft.objects.get_or_create(aircraft_code=code)
