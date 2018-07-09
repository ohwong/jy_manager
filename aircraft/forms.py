from django import forms
from .models import Aircraft


class AircraftChoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Aircraft

    def __init__(self, *args, **kwargs):
        super(AircraftChoiceAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['aircraft'].queryset = Aircraft.objects.valid_name_objects()
