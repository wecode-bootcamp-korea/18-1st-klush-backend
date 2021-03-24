import json
import random

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
            # product_id   = Product.objects.get(id=product_id) #등록할 상품의 정보 get으로 받음
            order_status = OrderStatus.objects.get(id=1) #status code 1 = 결제전

            if not Order.objects.filter(user_id=user_id, order_status=1).exists():

                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # 유저정보 일치, status 1번인 오더가 없을 때 새로 생성
                order = Order.objects.create(
                    order_number = ,
                    user_id = user_id,
                    order_status = order_status,
                )
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                OrderProduct.objects.create(
                    total_quantity = quantity,
                    product_id     = product_id,    
                    order_id       = order.id,
                )
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
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
            order_product.quantity += quantity
            order_product.save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)