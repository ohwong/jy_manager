from django.contrib import admin
from django.utils.html import mark_safe, strip_tags

from .models import DataStream
from .forms import DataStreamForm

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from date_range_filter import DateRangeFilter


class DataStreamResource(resources.ModelResource):

    class Meta:
        model = DataStream


class DataStreamAdmin(ImportExportModelAdmin):
    list_filter = ['the_year',  'the_month', 'the_day',  'aircraft_code', 'flight_type', 'location',
                   'weather', 'temperature',  'fault_type',
                   'chapter', 'knob', 'deal_method', 'is_sdr', "fault_result",
                   'has_delayed', 'has_checked', "status"]

    search_fields = ['fault_description', 'fault_type', 'chapter', 'knob', 'deal_method',
                      'record_paper_code', 'parts_name', 'strike_parts_code',
                      'strike_parts_num', 'mount_parts_code', 'fault_result']

    list_display = ['the_year', 'the_month', 'the_day', 'aircraft_code', 'location', 'chapter', 'knob',
                    'fault_phase', 'fault_description_strip', 'deal_method_strip', 'has_delayed', "status"]

    resource_class = DataStreamResource
    suit_form_tabs = (('base', '基本信息'), ('fault', '故障信息'), ('delay', '延误信息'),
                      ('deal', '处理信息'),)

    fieldsets = (


        ("基本信息", {
            'classes': ('suit-tab suit-tab-base',),
            'fields': ('aircraft_code', 'flight_type', 'the_year', 'the_month', 'the_day',
                       'location', 'weather', 'temperature', "status")
        }),
        ('故障信息', {
            'classes': ('suit-tab suit-tab-fault',),
            'fields': ('fault_phase', 'fault_type', 'fault_result',
                       'fault_description', ),
        }),
        ('延误信息', {
            'classes': ('suit-tab suit-tab-delay',),
            'fields': ('has_delayed',  'unexpected_stay_day',  'delay_time', 'delay_reason', ),
        }),
        ('处理信息', {
            'classes': ('suit-tab suit-tab-deal',),
            'fields': ('chapter', 'knob', 'is_sdr', 'record_paper_code', 'mel_or_cdl_file',
                       'parts_name', 'strike_parts_code', 'strike_parts_num', 'mount_parts_code',
                       'deal_method'),
        }),
    )

    add_fields = ['the_year',  'the_month', 'the_day', 'aircraft_code', 'flight_type', 'location',
                  'weather', 'temperature', 'fault_phase',
                  'fault_description', 'fault_type', 'chapter', 'knob', 'deal_method',
                  'record_paper_code', 'mel_or_cdl_file', 'parts_name', 'strike_parts_code',
                  'strike_parts_num', 'mount_parts_code', 'fault_result',
                  'delay_reason', 'delay_time', 'has_delayed', 'is_sdr', 'unexpected_stay_day',
                  "status"]

    change_fields = ['the_year',  'the_month', 'the_day', 'aircraft_code', 'flight_type', 'location',
                     'weather', 'temperature', 'fault_phase',
                     'fault_description', 'fault_type', 'chapter', 'knob', 'deal_method',
                     'record_paper_code', 'mel_or_cdl_file', 'parts_name', 'strike_parts_code',
                     'strike_parts_num', 'mount_parts_code', 'fault_result',
                     'delay_reason', 'delay_time', 'has_delayed', 'is_sdr', 'unexpected_stay_day',
                     "status"]

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

    def fault_description_strip(self, obj):
        return strip_tags(obj.fault_description)
    fault_description_strip.short_description = '故障描述'

    def deal_method_strip(self, obj):
        return strip_tags(obj.deal_method)
    deal_method_strip.short_description = '处理措施'

admin.site.register(DataStream, DataStreamAdmin)
