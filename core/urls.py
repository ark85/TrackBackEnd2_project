from django.conf.urls import url
from jsonrpc import jsonrpc_site

from core.views import index, Login, Logout, Register

urlpatterns = [
    url(r'^$', index),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^api/$', jsonrpc_site.dispatch, name="jsonrpc_mountpoint")
]
