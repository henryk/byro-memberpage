from django.conf.urls import include, url

from . import views

unprotected_urls = [
    url(r'^memberpage/(?P<secret_token>[^/]+)/$', views.MemberpageView.as_view(), name='memberpage.base'),
]

urlpatterns = [
    url(r'', include((unprotected_urls, 'unprotected'))),
]
