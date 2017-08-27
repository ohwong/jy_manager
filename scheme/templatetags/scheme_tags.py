
from django.template import Library
from scheme.models import MissionImage


register = Library()


@register.simple_tag
def current_scheme():
    """Converts a string into all lowercase"""
    try:
        return MissionImage.objects.last().image.url
    except AttributeError:
        return ""


