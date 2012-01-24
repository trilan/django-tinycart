from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from .models import Product


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Product)),
)
