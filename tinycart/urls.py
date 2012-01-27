from django.conf.urls.defaults import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^$',
        views.CartItemListView.as_view(),
        name='tinycart_cart_item_list'),
    url(r'^(?P<pk>\d+)/$',
        views.CartItemDetailView.as_view(),
        name='tinycart_cart_item_detail'),
)
