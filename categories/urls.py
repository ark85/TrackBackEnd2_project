from django.conf.urls import url
from jsonrpc import jsonrpc_site

from categories.views import CategoryEdit
from categories.views import CategoryCreate
from categories.views import CategoryViews
from categories.views import CategoryDetails


urlpatterns = [
    # url(r'^$', CategoryViews.as_view(), name='categories'),
    url(r'^(?P<category_id>\d+)/$', CategoryDetails.as_view(pk_url_kwarg='category_id'), name='category_details'),
    url(r'^(?P<category_id>\d+)/edit/$', CategoryEdit.as_view(pk_url_kwarg='category_id'), name='category_edit'),
    url(r'^create/$', CategoryCreate.as_view(), name='category_create'),
    url(r'^api/$', jsonrpc_site.dispatch, name="jsonrpc_mountpoint")
]
