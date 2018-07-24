from django.utils.timezone import now
from django.views.generic import DetailView

from byro.members.models import Member


class MemberpageView(DetailView):
    template_name = 'byro_memberpage/base.html'
    slug_field = 'profile_memberpage__secret_token'
    slug_url_kwarg = 'secret_token'

    model = Member

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = self.get_object()
        if not obj.memberships.count():
            return context
        first = obj.memberships.first().start
        delta = now().date() - first
        context['member_since'] = {
            'days': int(delta.total_seconds() / (60 * 60 * 24)),
            'years': round(delta.days / 365, 1),
            'first': first,
        }
        context['current_membership'] = obj.memberships.last()
        return context
