import json

from django.http      import JsonResponse
from django.views     import View

from user.models      import User
from product.models   import Product
from .models          import Order, OrderProduct, OrderStatus
from utils.decorator  import authorization

class OrderProductView(View):
    @authorization
    def post(self,request, product_id):

        try:
            data         = json.loads(request.body)
            user         = request.user
            quantity     = data['quantity']
            price        = data['price']
            product_id   = Product.objects.get(id=product_id)
            order_status = OrderStatus.objects.get(pk=1) #status code 1 = 결제전

            if not Order.objects.filter(user=user, order_status=1).exists():
            # 유저정보 일치, status 1번인 오더가 없을 때 새로 생성
                order = Order.objects.create(
                    order_number = order_number,
                    payment_id   = payment_id,
                    order_status = order_status,
                )
                OrderProduct.objects.create(
                    total_quantity = total_quantity,
                    product_id     = product_id,
                    order_id       = order_id,
                )
                return JsonResponse({'message':'SUCCESS'}, status=201)

            order = Order.objects.get(user=user, order_status=1)
            if not OrderProduct.objects.filter(order_id=order_id, product_id=product_id).exists():
                OrderProduct.objects.create(
                    total_quantity = total_quantity,
                    product_id     = product_id,
                    order_id       = order_id,
                )
                return JsonResponse({'message':'SUCCESS'}, status=201)

            order_product = OrderProduct.objects.get(order_id=order_id, product_id=product_id)
            order_product.quantity += int(quantity)
            order_product.save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)
