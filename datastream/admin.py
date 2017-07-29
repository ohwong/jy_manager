from django.contrib import admin

from .models import DataStream
from .forms import DataStreamForm

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from date_range_filter import DateRangeFilter


class DataStreamResource(resources.ModelResource):

    class Meta:
        model = DataStream


class DataStreamAdmin(ImportExportModelAdmin):
    list_filter = [('the_date', DateRangeFilter), 'aircraft_code', 'flight_type', 'location',
                   'weather', 'temperature',  'fault_type',
                   'chapter', 'knob', 'deal_method', 'is_sdr', "fault_result",
                   'has_delayed', 'has_checked', "status"]

    search_fields = ['fault_description', 'fault_type', 'chapter', 'knob', 'deal_method',
                      'record_paper_code', 'parts_name', 'strike_parts_code',
                      'strike_parts_num', 'mount_parts_code', 'fault_result']

    list_display = ['the_date', 'aircraft_code', 'location', 'chapter', 'knob',
                    'fault_phase', 'fault_description', 'deal_method', 'has_delayed', "status"]

    resource_class = DataStreamResource

    add_fields = ['the_date', 'aircraft_code', 'flight_type', 'location',
                  'weather', 'temperature', 'fault_phase',
                  'fault_description', 'fault_type', 'chapter', 'knob', 'deal_method',
                  'record_paper_code', 'mel_or_cdl_file', 'parts_name', 'strike_parts_code',
                  'strike_parts_num', 'mount_parts_code', 'fault_result',
                  'delay_reason', 'delay_time', 'has_delayed', 'is_sdr', 'unexpected_stay_day',
                  "status"]
              # exclude create_user create_time

    change_fields = ['the_date', 'aircraft_code', 'flight_type', 'location',
                    'weather', 'temperature', 'fault_phase',
                    'fault_description', 'fault_type', 'chapter', 'knob', 'deal_method',
                    'record_paper_code', 'mel_or_cdl_file', 'parts_name', 'strike_parts_code',
                    'strike_parts_num', 'mount_parts_code', 'fault_result',
                    'delay_reason', 'delay_time', 'has_delayed', 'is_sdr', 'unexpected_stay_day',
                     "status"]
              # exclude create_user create_time

    form = DataStreamForm

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        elif obj.create_user == request.user and obj.has_checked is False:
            return []
        return self.change_fields

    def get_fields(self, request, obj=None):
        if obj:
            return self.change_fields
        return self.add_fields

    def save_model(self, request, obj, form, change):

        if not change:
            obj.create_user = request.user
        return super(DataStreamAdmin, self).save_model(request, obj, form, change)

    actions = ['make_checked']

    def make_checked(self, request, queryset):
        if request.user.is_superuser:
            queryset.update(has_checked=True, check_user=request.user)
    make_checked.short_description = "完成审核"

    def has_change_permission(self, request, obj=None):
        # if request.user.is_superuser or (obj and obj.create_user == request.user):
        #     return True
        return True

    def get_queryset(self, request):
        qs = super(DataStreamAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(create_user=request.user)

admin.site.register(DataStream, DataStreamAdmin)
