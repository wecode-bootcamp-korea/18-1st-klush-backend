import json
import uuid

from django.http      import JsonResponse
from django.views     import View

from user.models      import User
from product.models   import Product, Image
from .models          import Order, OrderProduct, OrderStatus
from utils.decorator  import authorization

ORDER_STATUS = '결제전'

class CartView(View):
    @authorization
    def post(self,request, product_id):
        try: 
            data         = json.loads(request.body)
            user         = request.user
            quantity     = data['quantity']

            if not Order.objects.filter(user=user, order_status__status=ORDER_STATUS).exists():
                order=Order.objects.create(
                    order_number = uuid.uuid4(),
                    user         = user,
                    order_status = OrderStatus.objects.get(status=ORDER_STATUS),
                )
                OrderProduct.objects.create(
                    total_quantity = quantity,
                    product_id     = product_id,    
                    order_id       = order.id 
                )
                return JsonResponse({'message':'SUCCESS_CREATE'}, status=201)

            if not Order.objects.filter(user=user, order_status__status=ORDER_STATUS).exists():
                return JsonResponse({'message':'INVALID_ORDER'}, status=401)

            order = Order.objects.get(user=user, order_status__status=ORDER_STATUS)

            if OrderProduct.objects.filter(order=order, product_id=product_id).exists():
                order_product = OrderProduct.objects.get(order=order, product_id=product_id)
                order_product.total_quantity += quantity
                order_product.save()

                return JsonResponse({'message':'SUCCESS_ADD'}, status=200)

            OrderProduct.objects.create(
                    total_quantity = quantity,
                    product_id     = product_id,
                    order_id       = order.id
                )
            return JsonResponse({'message':'SUCCESS_CREATE'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400) 

        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)

    @authorization
    def get (self, request):
        try:
            user         = request.user

            if not Order.objects.filter(user=user, order_status__status=ORDER_STATUS).exists():
                return JsonResponse({'message':'INVALID_ORDER'}, status=401)
            
            order        = Order.objects.get(user=user, order_status__status=ORDER_STATUS)
            cart_lists   = order.orderproduct_set.all()
            
            cart_list = [
                {
                    "id"                : cart_list.id,
                    "sub_category_name" : cart_list.product.sub_category.name,
                    "price"             : cart_list.product.price,
                    "product_name"      : cart_list.product.name,
                    "quantity"          : cart_list.total_quantity,
                    "image_url"         : [image.image_url for image in cart_list.product.image_set.all()],
                } for cart_list in cart_lists
            ]

            return JsonResponse({'message':'SUCCESS', 'cart':cart_list},status=200)

        except OrderProduct.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST"}, status=400)
