from django import forms
from .models import DataStream
from django.contrib.admin import ListFilter
from django.contrib.auth import ImproperlyConfigured

YES_OR_NO = (
    (0, "否"),
    (1, "是"),
    (2, "是"),
)


class DataStreamForm(forms.ModelForm):
    class Meta:
        model = DataStream
        fields = ['the_year',  'the_month', 'the_day', 'aircraft_code', 'flight_type', 'location',
                  'weather', 'temperature', 'fault_phase',
                  'fault_description', 'fault_type', 'chapter', 'knob', 'deal_method',
                  'record_paper_code', 'mel_or_cdl_file', 'parts_name', 'strike_parts_code',
                  'strike_parts_num', 'mount_parts_code', 'fault_result',
                  'delay_reason', 'delay_time', 'has_delayed', 'is_sdr', 'unexpected_stay_day']


class SingleTextInputFilter(ListFilter):
    """
    renders filter form with text input and submit button
    """
    parameter_name = None
    template = "admin/textinput_filter.html"

    def __init__(self, request, params, model, model_admin):
        super(SingleTextInputFilter, self).__init__(
            request, params, model, model_admin)
        if self.parameter_name is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify "
                "a 'parameter_name'." % self.__class__.__name__)

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    def value(self):
        """
        Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return self.used_parameters.get(self.parameter_name, None)

    def has_output(self):
        return True

    def expected_parameters(self):
        """
        Returns the list of parameter names that are expected from the
        request's query string and that will be used by this filter.
        """
        return [self.parameter_name]

    def choices(self, cl):
        all_choice = {
            'selected': self.value() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name]),
            'display': 'All',
        }
        return ({
                    'get_query': cl.params,
                    'query_string': cl.get_query_string({}, [self.parameter_name]),
                    'current_value': self.value(),
                    'all_choice': all_choice,
                    'parameter_name': self.parameter_name
                }, )

