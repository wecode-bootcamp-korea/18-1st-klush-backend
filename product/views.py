import json

from django.http        import JsonResponse

from django.views       import View
from product.models     import Product, Image

class ProductListView(View):
    def get(self, request):
        try:            
            products     = Product.objects.all()
            product_list = []
            for product in products:
                dict = {
                    'sub_category'   : product.sub_category.name,
                    'name'           : product.name,
                    'image_url'      : [i.image_url for i in Image.objects.filter(product_id = product.id)], 
                    'price'          : product.price,
                    'is_vegan'       : product.is_vegan,
                    'is_new'         : product.is_new,
                    'is_soldout'     : product.is_soldout,
                    'product_label'  : product.label.name,
                    'product_id'     : product.id,
                }
                product_list.append(dict)

            return JsonResponse({'data' : product_list}, status = 200)
            
        except Product.DoesNotExist:
            return JsonResponse({'Message':'DOES_NOT_EXIST'}, status = 401)