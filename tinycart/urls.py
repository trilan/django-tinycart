from django.conf.urls.defaults import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^$',
        views.CartItemList.as_view(),
        name='tinycart_cart_item_list'),
)
