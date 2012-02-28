from boar.mailing_lists.tokens import default_token_generator as token_generator
import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse
from django.db import models
from ordered_model.models import OrderedModel
from smtplib import SMTPRecipientsRefused

class MailingList(OrderedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    from_email = models.EmailField(help_text="Address that emails appear to come from. Must be from the domain <em>theboar.org</em>.")
    template = models.TextField(blank=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='mailing_lists')
    default_for_new_users = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False, help_text="Is visible for users to select.")
    
    def __unicode__(self):
        return self.name


class Mailing(models.Model):
    mailing_list = models.ForeignKey(MailingList)
    subject = models.CharField(max_length=255, help_text='The subject for the email. It may be worth mentioning the name of your mailing list in the subject. For example, "Boar News: Yet another social next week"')
    message = models.TextField(help_text='The body of your email.')
    date_sent = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ('-date_sent',)

    def __unicode__(self):
        return '%s for %s' % (self.subject, self.mailing_list)
    
    def save(self, *args, **kwargs):
        created = not self.id
        super(Mailing, self).save(*args, **kwargs)
        if created:
            data = []
            for user in self.mailing_list.subscribers.all():
                if not user.email:
                    continue
                message = "%s\r\n\r\nIf you would prefer not to receive emails from the Boar's %s list, go here: http://theboar.org%s" % (
                    self.message,
                    self.mailing_list.name,
                    reverse('accounts_mailing_lists_unsubscribe', kwargs={
                        'user_id': user.id,
                        'mailing_list_id': self.mailing_list.id,
                        'token': token_generator.make_token(
                            user,
                            self.mailing_list,
                        ),
                    }),
                )
                data.append((
                    self.subject,
                    message,
                    self.mailing_list.from_email,
                    [user.email],
                ))
		try:
			send_mass_mail(datatuple=tuple(data), fail_silently=False)
		except SMTPRecipientsRefused:
			continue
		data = []


