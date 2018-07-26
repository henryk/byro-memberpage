import os

from annoying.fields import AutoOneToOneField
from django.db import models
from django.utils.baseconv import base56
from django.utils.translation import ugettext_lazy as _

from byro.common.models.choices import Choices
from byro.common.models.configuration import ByroConfiguration


def generate_default_token():
    return base56.encode(int.from_bytes(os.urandom(16), byteorder='big'))


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
    secret_token = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        default=generate_default_token,
    )
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
