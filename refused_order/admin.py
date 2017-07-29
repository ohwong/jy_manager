from django.contrib import admin
from .models import RefusedOrder

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from date_range_filter import DateRangeFilter


class RefusedOrderResource(resources.ModelResource):

    class Meta:
        model = RefusedOrder


class RefusedOrderAdmin(ImportExportModelAdmin):
    list_display = ['created_at', 'aircraft_code',  'terminal', 'worker_code',
                    'worker_content', 'apply_user', "deal_user",  'note',
                    'has_applied']

    change_fields = ['aircraft_code', 'terminal', 'worker_code',
                     'worker_content', 'note', 'has_applied']

    add_fields = ['aircraft_code', 'terminal', 'worker_code',
                  'worker_content', 'note']

    resource_class = RefusedOrderResource
    actions = ['make_checked']
    list_filter = [('created_at', DateRangeFilter), 'aircraft_code',
                   'terminal', 'worker_code', 'worker_content',
                   'apply_user', "deal_user",  'note', 'has_applied']

    search_fields = list_display

    def has_change_permission(self, request, obj=None):
        # if request.user.is_superuser or (obj and obj.apply_user == request.user):
        #     return True
        return True

    def get_queryset(self, request):
        qs = super(RefusedOrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(apply_user=request.user)

    def get_readonly_fields(self, request, obj=None):
        if obj is None or (request.user.is_superuser and obj.has_applied is False):
            # 没有批准过
            return []
        elif obj.apply_user == request.user and obj.has_applied is False:
            return []
        return self.change_fields

    def get_fields(self, request, obj=None):
        if obj:
            return self.change_fields
        return self.add_fields

    def make_checked(self, request, queryset):
        if request.user.is_superuser:
            queryset.update(has_applied=True, deal_user=request.user)
    make_checked.short_description = "处理申请"

    def save_model(self, request, obj, form, change):

        if not change:
            obj.apply_user = request.user
        elif request.user.is_superuser and obj.has_applied:
            obj.deal_user = request.user
        return super(RefusedOrderAdmin, self).save_model(request, obj, form, change)

admin.site.register(RefusedOrder, RefusedOrderAdmin)