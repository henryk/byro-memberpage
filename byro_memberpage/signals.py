# Register your receivers here
from django.dispatch import receiver

from byro.common.signals import unauthenticated_urls


@receiver(unauthenticated_urls)
def memberpage_unauthenticated_urls(sender, **kwargs):
    return (lambda a, b: b.view_name.startswith("plugins:byro_memberpage:unprotected:"), )
