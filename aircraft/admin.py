from django.contrib import admin


from .models import Aircraft


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('aircraft_code',)

    def has_delete_permission(self, request, obj=None):
        return False
