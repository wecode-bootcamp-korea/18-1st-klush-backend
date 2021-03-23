from django.urls import path

from .views      import OrderProductView

urlpatterns = [
    path('/add/<int:product_id>', OrderProductView.as_view()),
]
