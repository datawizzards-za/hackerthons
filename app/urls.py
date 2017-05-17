from django.conf.urls import url
from app.views import Help, UpdateTrasaction, LockTrasaction, UnlockTrasaction
from app.views import Dashboard, Analysis, Financials, Settings, Demo, Phone

uuid_pattern = '[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^\Z', Dashboard.as_view(), name='dashboard'),
    url(r'^' + uuid_pattern + '/$', Dashboard.as_view(), name='trans_verify'),
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^analysis/$', Analysis.as_view(), name='analysis'),
    url(r'^financials/$', Financials.as_view(), name='financials'),
    url(r'^settings/$', Settings.as_view(), name='settings'),
    url(r'^help/$', Help.as_view(), name='help'),
    url(r'^accept/(?P<ac>[0-9]+)/', UpdateTrasaction.as_view(), name='accept'),
    url(r'^lock/(?P<ac>[0-9]+)/', LockTrasaction.as_view(), name='lock'),
    url(r'^unlock/(?P<ac>[0-9]+)/', UnlockTrasaction.as_view(), name='unlock'),
    # url(r'^report/(?P<>[0-9]+)/',UpdateTrasaction.as_view(), name='report'),
    url(r'^demo/$', Demo.as_view(), name='demo'),
    url(r'^api_to_phone/(?P<ac>[0-9]+)/', Phone.as_view(), name='demo'),
]
