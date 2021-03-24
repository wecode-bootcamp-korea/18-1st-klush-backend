import json
from django.http     import JsonResponse

from django.views    import View
from product.models  import Menu, Category, Product, Image

class MainView(View):
    def get(self,request):
        try:
            targets = Product.objects.filter(is_new=1)
            new_product_list = []
            
            # 신상품 리스트를 필요 정보와 함께 가져온다.
            for target in targets:
                new_product_list.append(
                    {
                        "image_url" : [img.image_url for img in target.image_set.all()],
                        "name"      : target.name,
                        "label"     : target.label,
                        "price"     : target.price
                    }
                )
            return JsonResponse({'new_product_list':new_product_list},status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({'Message':'DoesNotExist',status=401})