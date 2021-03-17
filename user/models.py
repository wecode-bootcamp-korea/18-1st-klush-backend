from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=254, unique=True)
    password     = models.CharField(max_length=254)
    name         = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    nickname     = models.CharField(max_length=50, null=True, unique=True)

    class Meta:
        db_table = 'users'
