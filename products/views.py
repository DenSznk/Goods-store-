from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from products.models import Product, ProductCategory, Basket


class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Store'
        return context

# def index(request):
#     """Main page render"""
#
#     context = {
#         'title': 'Store'
#     }
#     return render(request, 'products/index.html', context)


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    ordering = 'price'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['title'] = 'Store Catalog'
        context['categories'] = ProductCategory.objects.all()
        return context

# def get_products(request, category_id=None):
#     """Receiving goods by category"""
#
#     if category_id:
#         page_obj = Product.objects.filter(category_id=category_id)
#         context = {
#             'title': 'Store catalog',
#             'categories': ProductCategory.objects.all(),
#             'page_obj': page_obj,
#         }
#         return render(request, 'products/products.html', context)
#     else:
#         products = Product.objects.prefetch_related('category').order_by('id')
#         lst = Paginator(products, 3)
#         page_number = request.GET.get('page')
#         page_obj = lst.get_page(page_number)
#     context = {
#         'title': 'Store catalog',
#         'categories': ProductCategory.objects.all(),
#         'page_obj': page_obj,
#     }
#     return render(request, 'products/products.html', context)


@login_required
def basket_add(request, pk):
    """adding product to basket"""

    product = Product.objects.get(id=pk)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, pk):
    """Remove goods from basket"""

    basket = Basket.objects.get(id=pk)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
