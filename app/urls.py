from django.conf.urls import url
from views import Dashboard, Analysis, Financials, Settings, Help

urlpatterns = [
    url(r'^\Z', Dashboard.as_view(), name='dashboard'),
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^analysis/$', Analysis.as_view(), name='analysis'),
    url(r'^financials/$', Financials.as_view(), name='financials'),
    url(r'^settings/$', Settings.as_view(), name='settings'),
    url(r'^help/$', Help.as_view(), name='help'),
]
