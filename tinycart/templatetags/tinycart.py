from django.contrib.contenttypes.models import ContentType
from django.template import Library


register = Library()


@register.filter
def content_type_pk(value):
    return ContentType.objects.get_for_model(value.__class__).pk
