from django.contrib import admin
from .models import Mission, MissionType, ThisMonthMission, MyMonthMission
from .utils import current_date_range


class MissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'mission_user', 'mission_type', 'start_date',
                    'end_date', 'status']

    change_readonly_fields = ['title', 'mission_user', 'mission_type', 'start_date',
                              'end_date', "description", "created_user"]

    add_fields = ['title', 'mission_user', 'mission_type', 'start_date',
                  'end_date', "description"]
    change_fields = ['title', 'mission_user', 'mission_type', 'start_date',
                     'end_date', "description", "created_user", "status"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return []
        return self.change_readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_user = request.user

        return super(MissionAdmin, self).save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        if obj:
            return self.change_fields
        return self.add_fields


class MissionTypeAdmin(admin.ModelAdmin):
    pass


class ThisMonthMissionAdmin(MissionAdmin):
    list_display = ['title', 'mission_user', 'mission_type', 'start_date',
                    'end_date', 'status']

    def get_queryset(self, request):
        qs = super(ThisMonthMissionAdmin, self).get_queryset(request)
        start_date, end_date = current_date_range()
        return qs.filter(end_date__gte=start_date, end_date__lte=end_date)

    change_readonly_fields = ['title', 'mission_user', 'mission_type', 'start_date',
                              'end_date', "description", "created_user"]

    def get_readonly_fields(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return []
        elif obj.mission_user != request.user:
            return self.change_readonly_fields + ['status']
        return self.change_readonly_fields


class MyMonthMissionAdmin(MissionAdmin):
    list_display = ['title', 'mission_user', 'mission_type', 'start_date',
                    'end_date', 'status']

    readonly_fields = ['title', 'mission_user', 'mission_type', 'start_date',
                       'end_date', "description", "created_user"]

    list_filter = ['status']

    actions = ['make_finished']

    def get_queryset(self, request):
        qs = super(MyMonthMissionAdmin, self).get_queryset(request)
        return qs.filter(mission_user=request.user)

    def make_finished(self, request, queryset):
        queryset.update(status=1)
    make_finished.short_description = "标记为完成"

admin.site.register(MissionType, MissionTypeAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(ThisMonthMission, ThisMonthMissionAdmin)
admin.site.register(MyMonthMission, MyMonthMissionAdmin)