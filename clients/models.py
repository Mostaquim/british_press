from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class OrderManager(models.Manager):
    def create_new_order(
        self,
        email, first_name, last_name, salutation, phone_prefix,
        house_number, street, zip_code, city,
        phone_number, item_id, comment
    ):
        user = User(
            email=email,
            username=email,
            password=None,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(None)
        user.save()
        client = Clients(
            user=user,
            salutation=salutation,
            phone_number=phone_number,
            phone_prefix=phone_prefix,
            house_number=house_number,
            zip_code=zip_code,
            city=city,
            street=street
        )
        client.save()

        order = Orders(
            client=client,
            item_id=item_id,
            order_confirmed=False,
            order_id=None,
            comment=comment
        )
        order.save()
        return order


class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salutation = models.CharField(max_length=5, null=True)
    phone_prefix = models.CharField(max_length=10, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    zip_code = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    house_number = models.CharField(max_length=255, null=True)


class Orders(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=255, null=True)
    order_confirmed = models.BooleanField()
    order_id = models.CharField(max_length=255, null=True)
    comment = models.TextField(null=True)

    objects = OrderManager()
