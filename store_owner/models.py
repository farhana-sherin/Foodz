from django.db import models


from users.models import User
from customer.models import *


class StoreOwner(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.email
    



