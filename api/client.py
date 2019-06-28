import setuptools
from django.conf import settings
from zeep.transports import Transport
from zeep.cache import SqliteCache
from requests import Session
from zeep import Client

class SoapClient(object):
    session = Session()
    session.verify = False
    session.cert = settings.CERTIFICATE_FILE
    cache = SqliteCache(path=settings.ZEEP_CACHE_PATH)
    transport = Transport(session=session)

    def get_catalog_client(self):
        client = Client(settings.CATALOGUE_WSDL , transport=self.transport)
        return client
    
    def get_order_client(self):
        client = Client(settings.ORDER_WSDL , transport=self.transport)
        return client

    def get_customer_client(self):
        client = Client(settings.CUSTOMER_WSDL , transport=self.transport)
        return client

    def get_tracking_client(self):
        client = Client(settings.TRACKING_WSDL , transport=self.transport)
        return client

  