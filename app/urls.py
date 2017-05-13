from django.conf.urls import url
from app.views import Dashboard, Analysis, Financials, Settings, Help


urlpatterns = [
    url(r'^\Z', Dashboard.as_view()),
    url(r'^dashboard$', Dashboard.as_view()),
    url(r'^analysis$', Analysis.as_view()),
    url(r'^financials$', Financials.as_view()),
    url(r'^settings$', Settings.as_view()),
    url(r'^help$', Help.as_view()),
]
