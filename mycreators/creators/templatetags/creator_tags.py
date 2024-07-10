from django import template
from creators.models import Creator

register = template.Library()

@register.simple_tag
def creator_status(user):
    try:
        creator = Creator.objects.get(user=user)
        return creator.status
    except Creator.DoesNotExist:
        return None