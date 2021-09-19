from django.shortcuts import render
import os, json

MODULE_DIR = os.path.dirname(__file__)


# Create your views here.


def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'products/index.html', context)


def products(request):
    file_path = os.path.join(MODULE_DIR, 'fixtures/db.json')
    context = {
        'title': 'geekshop',
        'products': json.load(open(file_path, encoding='utf-8'))
    }
    return render(request, 'products/products.html', context)
