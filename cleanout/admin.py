from django.contrib import admin
from .models import AirCraftCleanOut
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from date_range_filter import DateRangeFilter
from aircraft.admin import AircraftFormChoicesAdmin


class AirCraftCleanOutResource(resources.ModelResource):

    class Meta:
        model = AirCraftCleanOut


class AirCraftCleanOutAdmin(AircraftFormChoicesAdmin, ImportExportModelAdmin):
    list_display = ["aircraft", "aircraft_type", "cleanout_date", 'cleanout_method',
                    "cleanout_user", "cleanout_department", "cleanout_status",
                    "next_clieanout_date", "note"]

    fields = ["aircraft", "aircraft_type", "cleanout_date",
              "cleanout_department", "cleanout_method", "cleanout_status",
              "next_clieanout_date", "note"]

    resource_class = AirCraftCleanOutResource

    search_fields = ["aircraf", "aircraft_type",
                     "cleanout_user", "cleanout_department", "cleanout_status",
                     "cleanout_method"]

    list_filter = ["aircraft", "aircraft_type", "cleanout_date", 'cleanout_method',
                   "cleanout_user", "cleanout_department", "cleanout_status",
                   ("next_clieanout_date", DateRangeFilter)]

    def save_model(self, request, obj, form, change):

        if not change:
            obj.cleanout_user = request.user
        return super(AirCraftCleanOutAdmin, self).save_model(request, obj, form, change)


admin.site.register(AirCraftCleanOut, AirCraftCleanOutAdmin)
