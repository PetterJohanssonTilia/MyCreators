from django import template
from creators.models import Creator

register = template.Library()

@register.filter
def is_creator(user):
    return Creator.objects.filter(user=user).exists()