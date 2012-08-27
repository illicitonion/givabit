from amount_mismatch import AmountMismatch
from google.appengine.ext import db
from payment import IncomingPayment, OutgoingPayment, OutgoingPaymentState, Payment

class PaymentRepository(object):
    def __init__(self, donation_proportion_repository):
        self.donation_proportion_repository = donation_proportion_repository

    def add_incoming_payment(self, incoming_payment):
        incoming_payment.put()

    def get_next_expected_payments(self, user):
        """Gets the outgoing payments expected to be made when user makes their next full incoming payment."""
        donation_proportions = self.donation_proportion_repository.get_donation_proportions(user=user)
        total_amount_GBPennies = user.donation_amount
        total_proportions = reduce(lambda total, proportion: total + proportion.amount,
                                   donation_proportions,
                                   0)
        return map(lambda dp: Payment(charity=dp.charity, user=user, amount_GBPennies=total_amount_GBPennies * dp.amount / total_proportions),
                   donation_proportions)

    def get_pending_outgoing_payments(self, amount_mismatch_notifiers=None):
        """Gets outgoing payments for which incoming payments have been received (i.e. which are ready to be sent to charities).

        As a side effect, notifies any passed amount_mismatch_notifiers of any incoming/outgoing payment mismatches, i.e. incoming payments with insufficient outgoing payments pending, and outgoing payments with insufficient incoming payments pending.
        """
        if amount_mismatch_notifiers is None:
            amount_mismatch_notifiers = []

        all_donation_proportions = self.donation_proportion_repository.get_donation_proportions()

        donation_proportions_by_user = self._index(lambda dp: dp.user, all_donation_proportions)

        incoming_payments = self.get_incoming_payments()
        incoming_payments_by_user = self._index(lambda ip: ip.user, incoming_payments)

        users_to_payment_amounts = {}
        for user in set(donation_proportions_by_user.keys()).union(set(incoming_payments_by_user.keys())):
            one_user_incoming_payments = incoming_payments_by_user[user] if user in incoming_payments_by_user else []
            amount_paid_in = reduce(lambda total, ip: total + ip.amount_GBPennies,
                                    one_user_incoming_payments,
                                    0)
            amount_to_pay_out = user.donation_amount
            one_user_donation_proportions = donation_proportions_by_user[user] if user in donation_proportions_by_user else []
            total_proportions = reduce(lambda total, dp: total + dp.amount,
                                       one_user_donation_proportions,
                                       0)
            users_to_payment_amounts[user] = (amount_paid_in, amount_to_pay_out, total_proportions)

        problem_users = [user for user in users_to_payment_amounts.keys() if users_to_payment_amounts[user][0] != users_to_payment_amounts[user][1] or users_to_payment_amounts[user][2] <= 0]

        charity_amounts = {}
        for (user, donation_proportions) in donation_proportions_by_user.items():
            if user in problem_users:
                continue
            for dp in donation_proportions:
                (_, amount_to_pay_out, total_proportions) = users_to_payment_amounts[user]
                amount = amount_to_pay_out * dp.amount / total_proportions
                charity_amounts[dp.charity] = charity_amounts.setdefault(dp.charity, 0) + amount

        outgoing_payments = set()
        for (charity, amount_GBPennies) in charity_amounts.items():
            outgoing_payment = OutgoingPayment.new(charity=charity, amount_GBPennies=amount_GBPennies, status=OutgoingPaymentState.DISPLAYED)
            outgoing_payment.put()
            outgoing_payments.add(outgoing_payment)

        self.notify_mismatches(amount_mismatch_notifiers, problem_users, incoming_payments_by_user, donation_proportions_by_user, users_to_payment_amounts)

        return outgoing_payments

    def notify_mismatches(self, amount_mismatch_notifiers, users, incoming_payments_by_user, donation_proportions_by_user, users_to_payment_amounts):
        """Notifies all amount_mismatch_notifiers of all amount mismatches.

        Args:
        amount_mismatch_notifiers: [amount_mismatch_notifiers]
        invalid_payments_by_user: {user: [OutgoingPayment]}
        not_paid_up_users: {user: incoming_amount}
        """
        # TODO: This logic really shouldn't live here
        mismatches = []
        for user in users:
            (amount_paid_in, amount_to_pay_out, total_proportions) = users_to_payment_amounts[user]
            incoming_payments_by_user.setdefault(user, [])
            donation_proportions = donation_proportions_by_user[user] if user in donation_proportions_by_user else []
            outgoing_payments = map(lambda dp: OutgoingPayment.new(charity=dp.charity, amount_GBPennies=amount_to_pay_out * dp.amount / total_proportions, status=OutgoingPaymentState.VALUE_MISMATCH),
                                    donation_proportions)
            mismatches.append(AmountMismatch(user=user, incoming_GBPennies=amount_paid_in, outgoing=outgoing_payments))


        for notifier in amount_mismatch_notifiers:
            for mismatch in mismatches:
                notifier.notify(mismatch)

    def get_incoming_payments(self):
        return [ip for ip in IncomingPayment.all().run()]

    def _index(self, fn, xs):
        """Takes a list of xs and creates a dict of xs indexed by fn(x).

        Args:
            fn: lambda x -> y
            xs: x[]

        Return:
            dict{y: x[]}
        """
        ys = {}
        for x in xs:
            y = fn(x)
            if not y in ys:
                ys[y] = []
            ys[y].append(x)
        return ys
