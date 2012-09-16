from givabit.webapp.url import Url

from google.appengine.api import mail

class EmailService(object):
    def send_mail(self, to, subject, sender, body):
        mail.send_mail(to=to, subject=subject, sender=sender, body=body)

    def send_user_confirmation_mail(self, user):
        self.send_mail(to=user.email,
                       subject='Welcome to givabit',
                       sender='signup@givabit.org',
                       body='Please visit %s to confirm your account' % Url().for_page('confirmation', confirmation_code=user.confirmation_code, email=user.email, include_hostname=True),
                      )

