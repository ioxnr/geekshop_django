from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView

from geekshop.mixin import UserDispatchMixin
from products.models import Product
from baskets.models import Basket


# Create your views here.

# class BasketCreateView(CreateView, UserDispatchMixin):
#     model = Basket
#     fields = ['product']
#     template_name = 'products/products.html'
#     success_url = reverse_lazy('products:products')
#
#     def post(self, request, *args, **kwargs):
#         if 'product_id' in self.kwargs:
#             product_id = self.kwargs['product_id']
#             print(product_id)
#             user = request.user
#             product = Product.objects.get(id=product_id)
#             baskets = Basket.objects.filter(user=user, product=product)
#             if not baskets.exists():
#                 Basket.objects.create(user=user, product=product, quantity=1)
#             else:
#                 basket = baskets.first()
#                 basket.quantity += 1
#                 basket.save()
#
#             context = {
#                 'products': Product.objects.all()
#             }
#
#             result = render_to_string('baskets/baskets.html', context, request=request)
#             return JsonResponse({'result': result})
#
#         # return render(request, 'products/products.html', context)


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


# class BasketDeleteView(DeleteView, UserDispatchMixin):
#     model = Basket
#     success_url = reverse_lazy('users:profile')
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Basket, pk=self.request.product.pk)
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.is_active = False
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())

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
