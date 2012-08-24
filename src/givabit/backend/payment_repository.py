from payment import IncomingPayment, OutgoingPayment, Payment

class PaymentRepository(object):
    def add_payment(self, payment):
        payment.put()

    def add_incoming_payment(self, incoming_payment):
        incoming_payment.put()

    def get_pending_outgoing_payments(self):
        paid_up_users = self._get_paid_up_users()

        outgoing_payments_by_charity = {}
        for outgoing_payment in Payment.all().run():
            if not outgoing_payment.user in paid_up_users:
                #TODO: Investigate the trade-off between sending a giant WHERE user in (...) query vs grabbing everything and filtering in code
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
        return outgoing_payments

    def _get_incoming_payments_by_user(self):
        incoming_payments_by_user = {}
        for payment in IncomingPayment.all().run():
            if not payment.user in incoming_payments_by_user:
                incoming_payments_by_user[payment.user] = 0
            incoming_payments_by_user[payment.user] += payment.amount_GBPennies
        return incoming_payments_by_user

    def _get_paid_up_users(self):
        #TODO: Investigate caching Payment.all(), or something, because reading through the whole thing twice per get_pending_outgoing_payments sucks
        incoming_payments_by_user = {}
        for incoming_payment in IncomingPayment.all().run():
            if not incoming_payment.user in incoming_payments_by_user:
                incoming_payments_by_user[incoming_payment.user] = 0
            incoming_payments_by_user[incoming_payment.user] += incoming_payment.amount_GBPennies

        for outgoing_payment in Payment.all().run():
            if outgoing_payment.user in incoming_payments_by_user:
                incoming_payments_by_user[outgoing_payment.user] -= outgoing_payment.amount_GBPennies
        return [user for user in incoming_payments_by_user.keys() if incoming_payments_by_user[user] == 0]
