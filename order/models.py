from django.db      import models

from user.models    import User
from product.models import Product

class Order(models.Model):
    order_number = models.IntegerField()
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_add=True)
    total_price  = models.DecimalField(max_digits=10, decimal_places=2)
    payment      = models.OneToOneField('Payment', on_delete=models.CASCADE, null=True)
    user         = models.ForeignKey('user.User', on_delete=models.CASCADE)
    address      = models.ForeignKey('Address', on_delete=models.CASCADE, null=True)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table='orders'

class OrderProduct(models.Model):
    total_quantity = models.IntegerField()
    product        = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    order          = models.OneToOneField('Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders_products'

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_status'

class Shipping(models.Model):
    shipping_message = models.CharField(max_length=300,null=True)
    name             = models.CharField(max_length=50)
    phone_number     = models.CharField(max_length=50)
    address          = models.ForeignKey('Address',on_delete=models.CASCADE)
    user             = models.ForeignKey('user.User', on_delete=models.CASCADE)
    order            = models.OneToOneField('Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'shippings'

class Payment(models.Model):
    paid_at      = models.DateTimeField(auto_now_add=True)
    shipping_fee = models.DecimalField(max_digits=5, decimal_places=2)
    voucher      = models.ForeignKey('Vaucher', on_delete=models.CASCADE)
    method       = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE)

    class Meta:
        db_table ='payments'

class Vaucher(models.Model):
    name          = models.CharField(max_length=50)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table ='payments_methods'

class Address(models.Model):
    address = models.CharField(max_length=50)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table ='addresses'
