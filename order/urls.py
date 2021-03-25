from django.urls import path

from .views      import CartView

urlpatterns = [
    path('/cart/<int:product_id>', CartView.as_view()),
    path('/cart', CartView.as_view())

]