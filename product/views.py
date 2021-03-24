import json
from django.http        import JsonResponse

from django.views       import View
from product.models     import Product

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id = product_id).exists:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status = 401)

        product        = Product.objects.get(id = product_id)
        product_detail = [{
            'sub_category'  : product.sub_category.name,
            'product_id'    : product.id,
            'name'          : product.name,
            'price'         : product.price,
            'product_label' : [label.label.name for label in product.productlabel_set.all()],
            'image_url'     : [image.image_url for image in product.image_set.all()],
            'weight'        : product.weight,
            'detail'        : product.detail
        }]
        return JsonResponse({'product_detail_data': product_detail},status=200)