from django.contrib import admin


from .models import Aircraft


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('aircraft_code',)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(AircraftAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
