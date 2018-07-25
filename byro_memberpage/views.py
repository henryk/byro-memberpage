from datetime import timedelta

from django.db.models import Q
from django.utils.timezone import now
from django.views.generic import DetailView, ListView

from byro.bookkeeping.models import Booking
from byro.bookkeeping.special_accounts import SpecialAccounts
from byro.members.models import Member

from .models import MemberpageConfiguration, MemberViewLevel
from django.http import Http404


class MemberpageView(DetailView):
    slug_field = 'profile_memberpage__secret_token'
    slug_url_kwarg = 'secret_token'

    model = Member


class MemberpageView(MemberpageView):
    template_name = 'byro_memberpage/dashboard.html'

    def get_bookings(self, member):
        account_list = [SpecialAccounts.donations, SpecialAccounts.fees_receivable]
        return Booking.objects.with_transaction_data().filter(
            Q(debit_account__in=account_list) |
            Q(credit_account__in=account_list),
            member=member,
            transaction__value_datetime__lte=now(),
        ).order_by('-transaction__value_datetime')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context['member']
        _now = now()
        context['bookings'] = self.get_bookings(obj)
        memberships = obj.memberships.order_by('-start').all()
        if not memberships:
            return context
        first = memberships[0].start
        delta = timedelta()
        for ms in memberships:
            delta += (ms.end or _now.date()) - ms.start
            if not ms.end or ms.end <= _now.date():
                context['current_membership'] = ms
        context['memberships'] = memberships
        context['member_since'] = {
            'days': int(delta.total_seconds() / (60 * 60 * 24)),
            'years': round(delta.days / 365, 1),
            'first': first,
        }
        return context


class MemberpageListView(ListView):
    template_name = 'byro_memberpage/memberlist.html'
    paginate_by = 50
    context_object_name = 'members'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        config = MemberpageConfiguration.get_solo()
        context['memberpage_config'] = config
        context['member_view_level'] = MemberViewLevel
        context['member_undisclosed'] = Member.objects.exclude(profile_memberpage__visible_consent=True).count()
        return context

    def get_queryset(self):
        config = MemberpageConfiguration.get_solo()
        if config.can_see_other_members not in (MemberViewLevel.NAME_ONLY, MemberViewLevel.NAME_AND_CONTACT):
            raise Http404("Page does not exist")

        secret_token = self.kwargs.get('secret_token')
        if not secret_token:
            raise Http404("Page does not exist")
        
        member = Member.all_objects.filter(profile_memberpage__secret_token=secret_token).first()
        if not member:
            raise Http404("Page does not exist")

        if not member.is_active:
            raise Http404("Page does not exist")

        return Member.objects.filter(profile_memberpage__visible_consent=True)



