from django.db   import models

from user.models import User

class Menu(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "menus"

class Category(models.Model):
    name = models.CharField(max_length=50)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)

    class Meta:
        db_table = "categories"

class SubCategory(models.Model):
    name     = models.CharField(max_length=50)
    cagetory = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = "sub_categories"

class BrandArticle(models.Model):
    image_url = models.CharField(max_length=1000)
    title     = models.CharField(max_length=200)
    menu      = models.ForeignKey('Menu', on_delete=models.CASCADE)

class Product(models.Model):
    name           = models.CharField( max_length=50)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    weight         = models.DecimalField(max_digits=5, decimal_places=2) 
    quantity       = models.IntegerField(default=0)
    detail         = models.CharField(max_length=50) # html 어캐받음
    is_vegan       = models.BooleanField(default=False)
    is_new         = models.BooleanField(default=False)  
    soldout        = models.BooleanField(default=False)  
    sub_categories = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = "products"

class Image(models.Model):
    image_url = models.CharField(max_length=1000)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

class Like(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

class Label(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table='labels'

class ProductLabel(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    label   = models.ForeignKey('Label', on_delete=models.CASCADE)

    class Meta:
        db_table='products_labels'


    