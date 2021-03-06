# Register your receivers here
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from byro.common.signals import unauthenticated_urls
from byro.members.models import Member
from byro.members.signals import (
    new_member_mail_information, new_member_office_mail_information,
)
from byro.office.signals import nav_event

from .models import MemberpageConfiguration, MemberViewLevel


@receiver(unauthenticated_urls)
def memberpage_unauthenticated_urls(sender, **kwargs):
    return (lambda a, b: b.view_name.startswith("plugins:byro_memberpage:unprotected:"), )


@receiver(nav_event)
def memberpage_primary(sender, **kwargs):
    request = sender
    if request.resolver_match and request.resolver_match.view_name.startswith("plugins:byro_memberpage"):
        if 'secret_token' in request.resolver_match.kwargs:
            secret_token = request.resolver_match.kwargs['secret_token']
            kwargs = {'secret_token': secret_token}
            config = MemberpageConfiguration.get_solo()
            result = [
                {
                    'label': _('Member page'),
                    'url': reverse('plugins:byro_memberpage:unprotected:memberpage.dashboard', kwargs=kwargs),
                    'active': request.resolver_match.view_name == 'plugins:byro_memberpage:unprotected:memberpage.dashboard',
                }
            ]
            if config.can_see_other_members in (MemberViewLevel.NAME_ONLY, MemberViewLevel.NAME_AND_CONTACT):
                member = Member.all_objects.filter(profile_memberpage__secret_token=secret_token).first()
                if member.is_active:
                    result.append({
                        'label': _('Member list'),
                        'url': reverse('plugins:byro_memberpage:unprotected:memberpage.list', kwargs=kwargs),
                        'active': request.resolver_match.view_name == 'plugins:byro_memberpage:unprotected:memberpage.list',
                    })
            return result
    return {}


@receiver(new_member_mail_information)
def new_member_mail_info_memberpage(sender, signal, **kwargs):
    return _('Your personal member page is at {}').format(
        sender.profile_memberpage.get_url(),
    )


@receiver(new_member_office_mail_information)
def new_member_office_mail_info_memberpage(sender, signal, **kwargs):
    return _('Their personal member page is at {}').format(
        sender.profile_memberpage.get_url(),
    )
