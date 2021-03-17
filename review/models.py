from django.db      import models

from user.models    import User
from product.models import Product

class Review(models.Model):
    star_rating = models.CharField(max_length=254)
    content     = models.TextField(max_length=3000)
    product     = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'
    
    