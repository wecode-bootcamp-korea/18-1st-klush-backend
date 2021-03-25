import json

from django.http    import JsonResponse
from django.views   import View

from product.models import SubCategory, Product

class SubCategoryView(View):
    def get(self, request):
        sub_categories    = SubCategory.objects.all()

        sub_category_list = [{
            'sub_category'    : sub_category.id,
            'name'            : sub_category.name,
        } for sub_category in sub_categories]
        return JsonResponse({'sub_category_list_data' : sub_category_list}, status = 200)

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()

        is_new          = request.GET.get('is_new', None)
        sub_category_id = request.GET.get('sub_category', None)
        sort            = request.GET.get('sort', None)

        if sub_category_id:
            products = products.filter(sub_category_id=sub_category_id)

        if is_new:
            products = products.filter(is_new=is_new)

        if sort:
            products = products.order_by(sort)      
            
        product_list = [{
            'product_id'    : product.id,
            'sub_category'  : product.sub_category.name,
            'name'          : product.name,
            'images'        : [image.image_url for image in product.image_set.all()],
            'price'         : product.price,
            'is_vegan'      : product.is_vegan,
            'is_new'        : product.is_new,
            'is_soldout'    : product.is_soldout,
            'product_labels': [label.label.name for label in product.productlabel_set.all()],
        } for product in products]
        return JsonResponse({'product_list_data': product_list}, status=200)

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
