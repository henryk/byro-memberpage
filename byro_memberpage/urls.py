from django.conf.urls import include, url

from . import views

from django.conf.urls import include, url

unprotected_urls = [
    url(r'^memberpage$', views.TestView.as_view(), name='testview'),
]

urlpatterns = [
    url(r'', include((unprotected_urls, 'unprotected'))),
]
