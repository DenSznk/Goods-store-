from django.urls import path

from products.views import get_products, basket_add, basket_remove

urlpatterns = [
    path('', get_products, name='products'),
    path('<int:category_id>/', get_products, name='categories'),
    path('baskets/add/<int:pk>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:pk>/', basket_remove, name='basket_remove'),
]
