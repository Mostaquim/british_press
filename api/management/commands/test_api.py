from django.core.management import BaseCommand
from api.client import SoapClient
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        client = SoapClient().get_customer_client()

        
        customerProfile = {
            'email' : 'atest@test.com',
            'partyGroupName' : 'Marketize',
            'password' : '12345'

        }

        with client.settings(raw_response=True,xsd_ignore_sequence_order=True,):
            response = client.service.putProfile(
                environment=settings.ENVIRONMENT,
                customerProfile=customerProfile,
                messageLevel='all'
            )

            print(response)


