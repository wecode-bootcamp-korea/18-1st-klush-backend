import json

from django.http        import JsonResponse
from django.views       import View

from product.models     import Product, Image

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product        = Product.objects.get(id = product_id)
            product_detail = {
                'sub_category'  : product.sub_category.name,
                'product_id'    : product.id,
                'name'          : product.name,
                'price'         : product.price,
                'product_label' : product.label.name,
                'image_url'     : [i.image_url for i in Image.objects.filter(product_id = product.id)],
                'weight'        : product.weight,
                'detail'        : product.detail
            }
            return JsonResponse({'data': product_detail},status=200)
        except Product.DoesNotExist:
            return JsonResponse({'Message':'DOES_NOT_EXIST'}, status= 401)