from payment import OutgoingPayment, Payment

class PaymentRepository(object):
    def add_payment(self, payment):
        payment.put()

    def get_pending_outgoing_payments(self):
        payments = {}
        for payment in Payment.all().run():
            if not payment.charity in payments:
                payments[payment.charity] = 0
            payments[payment.charity] += payment.amount_GBPennies
        outgoing_payments = set()
        for (charity, amount_GBPennies) in payments.items():
            outgoing_payment = OutgoingPayment.new(charity=charity, amount_GBPennies=amount_GBPennies)
            outgoing_payment.put()
            outgoing_payments.add(outgoing_payment)
        return outgoing_payments
