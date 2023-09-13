import os
from base64 import decode

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restuarant.settings")
import django
django.setup()
from django.contrib.auth.models import User
from orders.models import *
# from users.models import *

# print(sum(x.amount for x in Item.objects.all()))
# carts = Item.objects.last()
# carts.amount += 1
# carts.save()
Cart(user=User.objects.last()).save
print(Cart.objects.all())