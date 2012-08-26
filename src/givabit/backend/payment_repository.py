from amount_mismatch import AmountMismatch
from payment import IncomingPayment, OutgoingPayment, OutgoingPaymentState, Payment

class PaymentRepository(object):
    def add_payment(self, payment):
        payment.put()

    def add_incoming_payment(self, incoming_payment):
        incoming_payment.put()

    def get_pending_outgoing_payments(self, amount_mismatch_notifiers=None):
        if amount_mismatch_notifiers is None:
            amount_mismatch_notifiers = []

        (paid_up_users, not_paid_up_users) = self._get_users_by_paid_up_status()

        outgoing_payments_by_charity = {}
        invalid_payments_by_user = {}

        for outgoing_payment in Payment.all().run():
            if not outgoing_payment.user in paid_up_users:
                if not outgoing_payment.user in invalid_payments_by_user:
                    invalid_payments_by_user[outgoing_payment.user] = []
                invalid_payments_by_user[outgoing_payment.user].append(OutgoingPayment.new(charity=outgoing_payment.charity, amount_GBPennies=outgoing_payment.amount_GBPennies, status=OutgoingPaymentState.VALUE_MISMATCH))
                continue

            charity = outgoing_payment.charity
            if not charity in outgoing_payments_by_charity:
                outgoing_payments_by_charity[charity] = 0
            outgoing_payments_by_charity[charity] += outgoing_payment.amount_GBPennies

        outgoing_payments = set()
        for (charity, amount_GBPennies) in outgoing_payments_by_charity.items():
            outgoing_payment = OutgoingPayment.new(charity=charity, amount_GBPennies=amount_GBPennies)
            outgoing_payment.put()
            outgoing_payments.add(outgoing_payment)

        self.notify_mismatches(amount_mismatch_notifiers, invalid_payments_by_user, not_paid_up_users)

        return outgoing_payments

    def notify_mismatches(self, amount_mismatch_notifiers, invalid_payments_by_user, not_paid_up_users):
        """Notifies all amount_mismatch_notifiers of all amount mismatches.

        Args:
        amount_mismatch_notifiers: [amount_mismatch_notifiers]
        invalid_payments_by_user: {user: [OutgoingPayment]}
        not_paid_up_users: {user: incoming_amount}
        """
        mismatches = []
        for user in set(invalid_payments_by_user.keys()).union(set(not_paid_up_users.keys())):
            not_paid_up_users.setdefault(user, 0)
            invalid_payments_by_user.setdefault(user, [])
            mismatches.append(AmountMismatch(user=user, incoming_GBPennies=not_paid_up_users[user], outgoing=invalid_payments_by_user[user]))

        for notifier in amount_mismatch_notifiers:
            for mismatch in mismatches:
                notifier.notify(mismatch)

    def _get_incoming_payments_by_user(self):
        incoming_payments_by_user = {}
        for payment in IncomingPayment.all().run():
            if not payment.user in incoming_payments_by_user:
                incoming_payments_by_user[payment.user] = 0
            incoming_payments_by_user[payment.user] += payment.amount_GBPennies
        return incoming_payments_by_user

    def _get_users_by_paid_up_status(self):
        # Returns ([paid_up_user], {not_paid_up_user: incoming_total})
        #TODO: Investigate caching Payment.all(), or something, because reading through the whole thing twice per get_pending_outgoing_payments sucks
        incoming_payments_by_user = {}
        for incoming_payment in IncomingPayment.all().run():
            already = 0
            if incoming_payment.user in incoming_payments_by_user:
                already = incoming_payments_by_user[incoming_payment.user][0]
            amount = already + incoming_payment.amount_GBPennies
            incoming_payments_by_user[incoming_payment.user] = (amount, amount)

        for outgoing_payment in Payment.all().run():
            if outgoing_payment.user in incoming_payments_by_user:
                already = incoming_payments_by_user[outgoing_payment.user]
                incoming_payments_by_user[outgoing_payment.user] = (already[0], already[1] - outgoing_payment.amount_GBPennies)

        paid_up_users, not_paid_up_users = [], {}
        for user in incoming_payments_by_user.keys():
            if incoming_payments_by_user[user][1] == 0:
                paid_up_users.append(user)
            else:
                not_paid_up_users[user] = incoming_payments_by_user[user][0]
        return (paid_up_users, not_paid_up_users)
