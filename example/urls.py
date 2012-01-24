from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^products/', include('products.urls')),
    url(r'^cart/', include('tinycart.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
