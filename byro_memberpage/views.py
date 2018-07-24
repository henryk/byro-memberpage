from django.views.generic import DetailView

from byro.members.models import Member


class MemberpageView(DetailView):
    template_name = 'byro_memberpage/base.html'
    slug_field = 'profile_memberpage__secret_token'
    slug_url_kwarg = 'secret_token'

    model = Member
