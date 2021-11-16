from django.shortcuts import render, get_object_or_404
import os, json

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache

MODULE_DIR = os.path.dirname(__file__)


# Create your views here.


def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'products/index.html', context)


def get_category_links():
    if settings.LOW_CACHE:
        key = 'category_links'
        category_links = cache.get(key)
        if category_links is None:
            category_links = ProductCategory.objects.all()
            cache.set(key, category_links)
        return category_links
    else:
        return ProductCategory.objects.all()


def get_product_links():
    if settings.LOW_CACHE:
        key = 'product_links'
        product_links = cache.get(key)
        if product_links is None:
            product_links = Product.objects.all().select_related('category')
            cache.set(key, product_links)
        return product_links
    else:
        return Product.objects.all().select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    success_url = reverse_lazy('products:index')

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['categories'] = get_category_links()
        category_id = None
        page_id = 1

        if 'category_id' in self.kwargs:
            category_id = self.kwargs['category_id']

        if 'page_id' in self.kwargs:
            page_id = self.kwargs['page_id']

        products = Product.objects.filter(category_id=category_id).select_related('category').order_by('id') \
            if category_id is not None else Product.objects.all().select_related('category').order_by('id')

        paginator = Paginator(products, per_page=3)

        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['products'] = products_paginator

        return context


# def products(request, category_id=None, page_id=1):
#     # file_path = os.path.join(MODULE_DIR, 'fixtures/db.json')
#     products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()
#
#     paginator = Paginator(products, per_page=3)
#     try:
#         products_paginator = paginator.page(page_id)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#
#     context = {
#         'title': 'Каталог',
#         'products': products_paginator,
#         'categories': ProductCategory.objects.all()
#         # 'products': json.load(open(file_path, encoding='utf-8'))
#     }
#     return render(request, 'products/products.html', context)

class ProductDetail(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()

        context['product'] = get_product(self.kwargs.get('pk'))
        context['categories'] = ProductCategory.objects.all()
        return context
