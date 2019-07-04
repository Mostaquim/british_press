import json
from django.core.management import BaseCommand
from formpage.models import CatalogPage
from api.client import SoapClient
from django.conf import settings
from zeep.helpers import serialize_object
from api.models import ApiCache


class Command(BaseCommand):

    def handle(self, *args, **options):
        catalogs = CatalogPage.objects.all()
        client = SoapClient().get_catalog_client()

        for catalog in catalogs:
            selected = {
                'optionIds': [
                    {
                        'name': 'product',
                        'value': catalog.api_value
                    }
                ],
                'shippingDestinationChoice': 0,
            }
            print(selected)

            with client.settings(strict=False):
                response = client.service.getCustomCatalogue(
                    environment=settings.ENVIRONMENT,
                    selected=selected,
                    messageLevel='all'
                )

                content = json.dumps(serialize_object(response.productList))
                cache = ApiCache.objects.filter(product=catalog.api_value)

                if cache.exists():
                    cache.response = content
                    cache.save()
                else:
                    cache = ApiCache(
                        product=catalog.api_value,
                        response=content
                    )

                    cache.save()
