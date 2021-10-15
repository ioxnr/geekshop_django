from django.shortcuts import render
import os, json

from django.urls import reverse_lazy
from django.views.generic import ListView

from .models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

MODULE_DIR = os.path.dirname(__file__)


# Create your views here.


def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'products/index.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    success_url = reverse_lazy('products:index')

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['categories'] = ProductCategory.objects.all()

        category_id = None
        page_id = 1

        if 'category_id' in self.kwargs:
            category_id = self.kwargs['category_id']

        if 'page_id' in self.kwargs:
            page_id = self.kwargs['page_id']

        products = Product.objects.filter(category_id=category_id) if category_id is not None else Product.objects.all()

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
