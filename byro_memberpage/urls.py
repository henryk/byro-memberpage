from django.conf.urls import include, url

from . import views

memberpage_urls = [
    url(r'^$', views.MemberpageView.as_view(), name='memberpage.dashboard'),
    url(r'^member_list$', views.MemberpageListView.as_view(), name='memberpage.list'),
]

unprotected_urls = [
    url(r'^memberpage/(?P<secret_token>[^/]+)/', include((memberpage_urls))),
]

urlpatterns = [
    url(r'', include((unprotected_urls, 'unprotected'))),
]
