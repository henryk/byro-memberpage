from annoying.fields import AutoOneToOneField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from byro.common.models.choices import Choices
from byro.common.models.configuration import ByroConfiguration


class MemberViewLevel(Choices):
    NO = 'no'
    NAME_ONLY = 'name-only'
    NAME_AND_CONTACT = 'name-contact'


class MemberpageProfile(models.Model):
    form_title = _("Memberpage settings")

    member = AutoOneToOneField(
        to='members.Member',
        on_delete=models.CASCADE,
        related_name='profile_memberpage',
    )
    secret_token = models.CharField(max_length=128, null=True, blank=True)
    visible_consent = models.BooleanField(
        default=False,
        verbose_name=_('Consent: Visible to other members'),
    )


class MemberpageConfiguration(ByroConfiguration):
    form_title = _("Memberpage configuration")

    can_see_other_members = models.CharField(
        max_length=MemberViewLevel.max_length,
        verbose_name=_('Members can see other members'),
        choices=MemberViewLevel.choices,
        default=MemberViewLevel.NO,
    )
