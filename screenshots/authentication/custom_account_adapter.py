from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):

        """
            TODO: Changing the FRONT_END_BASE_URL EnvVar to point to the correct URL
        """

        return f'{settings.FRONT_END_BASE_URL}/verify-account/{emailconfirmation.key}'
