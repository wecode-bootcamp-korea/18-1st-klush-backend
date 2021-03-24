from django.urls   import path

from .views        import ProductListView, SubCategoryView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/category', SubCategoryView.as_view()),
]