from django.urls   import path
from .views        import ProductListView

urlpatterns = [
    path('/product-list', ProductListView.as_view()),
]