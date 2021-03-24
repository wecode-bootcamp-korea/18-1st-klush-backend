import json
from django.http        import JsonResponse

from django.views       import View
from product.models     import Product, Image

class ProductListView(View):
    def get(self, request):
        products     = Product.objects.all()
        product_list = [{
            'sub_category'   : product.sub_category.name,
            'name'           : product.name,
            'image_url'      : [i.image_url for i in Image.objects.filter(product_id = product.id)],
            'price'          : product.price,
            'is_vegan'       : product.is_vegan,
            'is_new'         : product.is_new,
            'is_soldout'     : product.is_soldout,
            'product_label'  : [l.label.name for l in product.productlabel_set.all()],
            'product_id'     : product.id,
        } for product in products]
        return JsonResponse({'product_list_data' : product_list}, status = 200)