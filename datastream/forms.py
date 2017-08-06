from django import forms
from .models import DataStream

YES_OR_NO = (
    (0, "否"),
    (1, "是"),
    (2, "是"),
)


class DataStreamForm(forms.ModelForm):
    class Meta:
        model = DataStream
        fields = ['the_date', 'aircraft_code', 'flight_type', 'location',
                  'weather', 'temperature', 'fault_phase',
                  'fault_description', 'fault_type', 'chapter', 'knob', 'deal_method',
                  'record_paper_code', 'mel_or_cdl_file', 'parts_name', 'strike_parts_code',
                  'strike_parts_num', 'mount_parts_code', 'fault_result',
                  'delay_reason', 'delay_time', 'has_delayed', 'is_sdr', 'unexpected_stay_day']
