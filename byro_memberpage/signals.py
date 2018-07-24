# Register your receivers here
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import ugettext_lazy as _

from byro.common.signals import unauthenticated_urls
from byro.office.signals import nav_event


@receiver(unauthenticated_urls)
def memberpage_unauthenticated_urls(sender, **kwargs):
    return (lambda a, b: b.view_name.startswith("plugins:byro_memberpage:unprotected:"), )


@receiver(nav_event)
def memberpage_primary(sender, **kwargs):
    request = sender
    if request.resolver_match and request.resolver_match.view_name.startswith("plugins:byro_memberpage"):
        if 'secret_token' in request.resolver_match.kwargs:
            kwargs = {'secret_token': request.resolver_match.kwargs['secret_token']}
            return [
                {
                    'label': _('Member page'),
                    'url': reverse('plugins:byro_memberpage:unprotected:memberpage.dashboard', kwargs=kwargs),
                    'active': request.resolver_match.view_name == 'plugins:byro_memberpage:unprotected:memberpage.dashboard',
                }, {
                    'label': _('Finance details'),
                    'url': reverse('plugins:byro_memberpage:unprotected:memberpage.finance', kwargs=kwargs),
                    'active': request.resolver_match.view_name == 'plugins:byro_memberpage:unprotected:memberpage.finance',
                }
            ]
    return {}
