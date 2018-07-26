import os
import urlparse

from annoying.fields import AutoOneToOneField
from django.db import models
from django.urls import reverse
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

    def get_url(self):
        config = MemberpageConfiguration.get_solo()
        relative_url = reverse(
            'plugins:byro_memberpage:unprotected:memberpage.dashboard',
            kwargs={'secret_token': self.secret_token}
        )
        if config.external_base_url:
            return urlparse.urljoin(config.external_base_url, relative_url)
        else:
            return relative_url


class MemberpageConfiguration(ByroConfiguration):
    form_title = _("Memberpage configuration")

    external_base_url = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name=_("External base URL of byro installation"),
        help_text=_("This field is used to generate the absolute URL for memberpage addresses."),
    )
    can_see_other_members = models.CharField(
        max_length=MemberViewLevel.max_length,
        verbose_name=_('Members can see other members'),
        choices=MemberViewLevel.choices,
        default=MemberViewLevel.NO,
    )
