import os
from clients.models import Orders
from django.conf import settings

def create_item_id(formData):
    i=1
    z= True
    while z:
        item_id = "%s_%s_%s" % (formData['firstName'],formData['lastName'],i)
        item_id = item_id.replace(' ', '_')
        o = Orders.objects.filter(item_id=item_id)
        if not o.exists():
            return item_id
        i+=1

def handle_uploaded_file(f):
    main_path = os.path.join(settings.UPLOAD_DIR,  f.name)
    with open(main_path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)