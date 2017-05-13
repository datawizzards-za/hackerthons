from django.conf.urls import url
from views import Home

urlpatterns = [
    url(r'^\Z', Home.as_view(), name='index'),
]