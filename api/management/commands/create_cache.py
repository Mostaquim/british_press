import json
from django.core.management import BaseCommand
from formpage.models import CatalogPage, ApiCache
from api.client import SoapClient
from django.conf import settings
from zeep.helpers import serialize_object
from api.helper import get_selected



class Command(BaseCommand):

    def handle(self, *args, **options):
        catalogs = CatalogPage.objects.all()
        client = SoapClient().get_catalog_client()

        for catalog in catalogs:
            selected = json.loads(catalog.api_value)
            print(selected)

            with client.settings(strict=False):
                response = client.service.getCustomCatalogue(
                    environment=settings.ENVIRONMENT,
                    selected=selected,
                    messageLevel='all'
                )

                content = json.dumps(get_selected(serialize_object(response.productList)))
                cache = ApiCache.objects.filter(product=catalog)

                if cache.exists():
                    cache = cache[0]
                    cache.response = content
                    cache.save()
                else:
                    cache = ApiCache(
                        product=catalog,
                        response=content
                    )

                    cache.save()
