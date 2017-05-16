from django.conf.urls import url
from views import Dashboard, Analysis, Financials, Settings, Help, Demo

uuid_pattern = '[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}'
urlpatterns = [
    url(r'^\Z', Dashboard.as_view(), name='dashboard'),
    url(r'^'+uuid_pattern+'/$', Dashboard.as_view(), name='trans_verify'),
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^analysis/$', Analysis.as_view(), name='analysis'),
    url(r'^financials/$', Financials.as_view(), name='financials'),
    url(r'^settings/$', Settings.as_view(), name='settings'),
    url(r'^help/$', Help.as_view(), name='help'),
    url(r'^demo/$', Demo.as_view(), name='demo'),
]
