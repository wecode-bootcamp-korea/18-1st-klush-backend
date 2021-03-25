import json
import uuid

from django.http      import JsonResponse
from django.views     import View

from user.models      import User
from product.models   import Product, Image
from .models          import Order, OrderProduct, OrderStatus
from utils.decorator  import authorization

class OrderProductView(View):
    @authorization
    def post(self,request, product_id):

        try: #키값: 이미지, 카테고리, 수량, 가격,아이디값, 제품명
            data         = json.loads(request.body)
            user         = request.user
            quantity     = data['quantity']
            order_status = OrderStatus.objects.get(id=1) #status code 1 = 결제전
            print(user)
            if not Order.objects.filter(user=user, order_status=order_status).exists():
                print("**************************************")
            # 유저정보 일치, status 1번인 오더가 없을 때 오더와 오더프로덕트새로 생성
                order=Order.objects.create(
                    order_number = uuid.uuid4(),
                    user         = user,
                    order_status = order_status,
                )
                print(user.name)
                OrderProduct.objects.create(
                    total_quantity = quantity,
                    product_id     = product_id,    
                    order_id       = order.id #계속 2로 출력
                )
                return JsonResponse({'message':'SUCCESS'}, status=201)
                print(order_id)

            order = Order.objects.get(user=user, order_status=order_status)
            print(order)
            #수량 추가
            if OrderProduct.objects.filter(order=order, product_id=product_id).exists():
                order_product = OrderProduct.objects.get(order=order, product_id=product_id)
                order_product.total_quantity += quantity
                order_product.save()

                return JsonResponse({'message':'SUCCESS_ADD'}, status=200)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            # 오더는 있지만 오더프로덕트가 없을때
            OrderProduct.objects.create(
                    total_quantity = quantity,
                    product_id     = product_id,
                    order_id       = order.id
                )
            return JsonResponse({'message':'SUCCESS_CREATE'}, status=201)
            print("########################################")
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400) 

        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)

    @authorization
    def get (self, request):
        try:
            user = request.user
            print(user.name)
            order = Order.objects.get(user=user, order_status=1)
            print(order)
            cart_lists = order.orderproduct_set.all()
            print(cart_lists)
            
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
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST", "items_in_cart":[]}, status=400)
