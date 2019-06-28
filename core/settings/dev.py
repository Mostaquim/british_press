from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sg=3^$#xvfdg+5_-#*s@nrukqb@!4z697=yb&@qgp=v=(_6$y!'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WSDL_URL = 'http://interface.unitedprint.com.onts.print24test.de/wsdl2.1/'

CATALOGUE_WSDL =  WSDL_URL + 'catalogue.wsdl'
ORDER_WSDL =  WSDL_URL + 'order.wsdl'
CUSTOMER_WSDL =  WSDL_URL + 'customer.wsdl'
TRACKING_WSDL =  WSDL_URL + 'tracking.wsdl'

CERTIFICATE_FILE = os.path.join(BASE_DIR, 'marketize_dev.cert')

ENVIRONMENT = {
    'languageCode': 'en',
    'countryCode': 'GB',
    'portalName': 'print24',
    'partyGroupName': 'marketize',
}


ZEEP_CACHE_PATH = os.path.join(BASE_DIR, 'zeep_cache.db')

try:
    from .local import *
except ImportError:
    pass
