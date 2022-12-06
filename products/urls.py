from django.urls import path

from products.views import ProductsListView, basket_add, basket_remove

urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('<int:category_id>/', ProductsListView.as_view(), name='categories'),
    path('baskets/add/<int:pk>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:pk>/', basket_remove, name='basket_remove'),
]
