from django.contrib import admin
from .models import AirCraftCleanOut
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class AirCraftCleanOutResource(resources.ModelResource):

    class Meta:
        model = AirCraftCleanOut


class AirCraftCleanOutAdmin(ImportExportModelAdmin):
    list_display = ["aircraft_code", "aircraft_type", "cleanout_date",
                    "cleanout_user", "cleanout_department", "cleanout_status",
                    "next_clieanout_date", "note"]

    fields = ["aircraft_code", "aircraft_type", "cleanout_date",
              "cleanout_department", "cleanout_status",
              "next_clieanout_date", "note"]

    resource_class = AirCraftCleanOutResource

    search_fields = ["aircraft_code", "aircraft_type", "cleanout_date",
                     "cleanout_user", "cleanout_department", "cleanout_status",
                     "next_clieanout_date"]
    list_filter = search_fields

    def save_model(self, request, obj, form, change):

        if not change:
            obj.cleanout_user = request.user
        return super(AirCraftCleanOutAdmin, self).save_model(request, obj, form, change)


admin.site.register(AirCraftCleanOut, AirCraftCleanOutAdmin)
