from django.conf import settings
from django.utils.hashcompat import sha_constructor
 
class UnsubscribeTokenGenerator(object):
    def make_token(self, user, mailing_list):
        """
        Returns a token that can be used once to do an unsubscribe 
        for the given user.
        """
        # We limit the hash to 20 chars to keep URL short
        return sha_constructor(settings.SECRET_KEY + unicode(user.id)
                               + unicode(mailing_list.id)).hexdigest()[::2]
    
    def check_token(self, user, mailing_list, token):
        """
        Check that a password reset token is correct for a given user.
        """
        # Check that the mailing list/uid has not been tampered with
        if self.make_token(user, mailing_list) != token:
            return False
        return True
 
 
default_token_generator = UnsubscribeTokenGenerator()
