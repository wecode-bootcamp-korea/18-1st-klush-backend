import json
import uuid

from django.http      import JsonResponse
from django.views     import View

from user.models      import User
from product.models   import Product
from .models          import Order, OrderProduct, OrderStatus
from utils.decorator  import authorization

class OrderProductView(View):
    @authorization
    def post(self,request, product_id):

        try: #키값: 이미지, 카테고리, 수량, 가격,아이디값, 제품명
            data         = json.loads(request.body)
            user_id      = request.user.id
            quantity     = data['quantity']
            order_status = OrderStatus.objects.get(id=1) #status code 1 = 결제전

            if not Order.objects.filter(user_id=user_id, order_status=1).exists():

            # 유저정보 일치, status 1번인 오더가 없을 때 새로 생성
                order = Order.objects.create(
                    order_number = uuid.uuid4(),
                    user_id = user_id,
                    order_status = order_status,
                )
                OrderProduct.objects.create(
                    total_quantity = quantity,
                    product_id     = product_id,    
                    order_id       = order.id,
                )
                return JsonResponse({'message':'SUCCESS'}, status=201)

            order = Order.objects.get(user_id=user_id, order_status=1)
            if not OrderProduct.objects.filter(order=order, product_id=product_id).exists():
                OrderProduct.objects.create(
                    total_quantity = quantity,
                    product_id     = product_id,
                    order_id       = order.id,
                )
                return JsonResponse({'message':'SUCCESS_CREATE'}, status=201)

            order_product = OrderProduct.objects.get(order=order, product_id=product_id)
            order_product.total_quantity += quantity
            order_product.save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)

    def get (self, request):
        try:
            user_id = request.GET['user_id']
            print(user_id)
            order = Orders.objects.filter(user=user, order_status=1)
            cart_lists = order.orderproduct_set.all()
            
            cart_list = [{
                "id": carts.id,
                "sub_category_name": Product.sub_category.name,
                "price": carts.product.price,
                "product_name": carts.product.name,
                "quantity": carts.total_quantity,
                "image_url": [i.image_url for i in Image.objects.filter(product_id = product.id)],
            } for car_list in cart_lists]

            return JsonResponse({'message':'SUCCESS', 'cart':cart_list},status=200)

        except OrderProduct.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST", "items_in_cart":[]}, status=400)