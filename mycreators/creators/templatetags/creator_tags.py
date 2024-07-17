from django import template
from django.contrib.auth.models import AnonymousUser
from creators.models import Creator

register = template.Library()

@register.simple_tag
def creator_status(user):
    if isinstance(user, AnonymousUser):
        return None
    try:
        creator = Creator.objects.get(user=user)
        return creator.status
    except Creator.DoesNotExist:
        return None