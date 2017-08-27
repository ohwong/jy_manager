
from django.template import Library
from scheme.models import MissionImage


register = Library()


@register.simple_tag
def current_scheme():
    """Converts a string into all lowercase"""

    return MissionImage.objects.last().image.url
