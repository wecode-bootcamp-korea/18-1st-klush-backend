from django.urls   import path

from .views        import ProductListView, ProductDetailView, SubCategoryView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/subcategory', SubCategoryView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]