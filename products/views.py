from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from products.models import Product, ProductCategory, Basket


def index(request):
    """Main page render"""

    context = {
        'title': 'Store'
    }
    return render(request, 'products/index.html', context)


def get_products(request, category_id=None):
    """Receiving goods by category"""

    if category_id:
        page_obj = Product.objects.filter(category_id=category_id)
        context = {
            'title': 'Store catalog',
            'categories': ProductCategory.objects.all(),
            'page_obj': page_obj,
        }
        return render(request, 'products/products.html', context)
    else:
        products = Product.objects.prefetch_related('category').order_by('id')
        lst = Paginator(products, 3)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
    context = {
        'title': 'Store catalog',
        'categories': ProductCategory.objects.all(),
        'page_obj': page_obj,
    }
    return render(request, 'products/products.html', context)


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
