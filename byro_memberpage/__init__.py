from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'byro_memberpage'
    verbose_name = 'Byro plugin for member-visible view'

    class ByroPluginMeta:
        name = ugettext_lazy('Byro plugin for member-visible view')
        author = 'Henryk Plötz'
        description = ugettext_lazy('A byro plugin that allows each member to see information about their membership status. Login is via a specific secret link.')
        visible = True
        version = '0.0.1'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'byro_memberpage.PluginApp'
