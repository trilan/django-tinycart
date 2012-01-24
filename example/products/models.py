from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    is_in_stock = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
