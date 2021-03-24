from django.urls import path

from .views      import OrderProductView

urlpatterns = [
    path('/cart/<int:product_id>', OrderProductView.as_view())
]