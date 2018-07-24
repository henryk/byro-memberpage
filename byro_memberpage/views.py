from django.db.models import Q
from django.utils.timezone import now
from django.views.generic import DetailView

from byro.bookkeeping.models import Booking
from byro.bookkeeping.special_accounts import SpecialAccounts
from byro.members.models import Member


class MemberpageView(DetailView):
    slug_field = 'profile_memberpage__secret_token'
    slug_url_kwarg = 'secret_token'

    model = Member


class MemberpageView(MemberpageView):
    template_name = 'byro_memberpage/dashboard.html'

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


class MemberpageFinanceView(MemberpageView):
    template_name = 'byro_memberpage/finance.html'
    paginate_by = 50

    def get_bookings(self):
        account_list = [SpecialAccounts.donations, SpecialAccounts.fees_receivable]
        return Booking.objects.with_transaction_data().filter(
            Q(debit_account__in=account_list) |
            Q(credit_account__in=account_list),
            member=self.get_object(),
            transaction__value_datetime__lte=now(),
        ).order_by('-transaction__value_datetime')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['member'] = self.get_object()
        context['bookings'] = self.get_bookings()
        return context
