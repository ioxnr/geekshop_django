from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.template.loader import render_to_string

from products.models import Product
from baskets.models import Basket


# Create your views here.

@login_required
def basket_add(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, product_id):
    Basket.objects.get(id=product_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=pk)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {
            'baskets': baskets
        }
        result = render_to_string('baskets/baskets.html', context)
        return JsonResponse({'result': result})
