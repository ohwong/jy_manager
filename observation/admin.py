from django.contrib import admin

from .models import Observation
from date_range_filter import DateRangeFilter


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'aircraft_code', 'item_code', 'sort_code',
                    'tear_data', 'work_user', 'observation_days',
                    'estimated_closing_date', 'closed_date', 'closed_user',
                    'tear_reason', 'observation_result']

    list_filter = ['name', 'aircraft_code', 'item_code', 'sort_code',
                    'tear_data', 'work_user', 'observation_days', 'closed_user',
                    'tear_reason', 'observation_result',
                   ('estimated_closing_date', DateRangeFilter),
                   ('closed_date', DateRangeFilter)]

    add_fields = ['name', 'aircraft_code', 'item_code', 'sort_code',
                  'tear_data', 'work_user', 'observation_days',
                  'estimated_closing_date', 'closed_date', 'closed_user',
                  'tear_reason', 'observation_result']

    change_fields = list_display

    def get_fields(self, request, obj=None):
        if obj:
            return self.change_fields
        return self.add_fields

    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.work_user = request.user
    #     return super(ObservationAdmin, self).save_model(request, obj, form, change)