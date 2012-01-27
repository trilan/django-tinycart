from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin

from .forms import CartItemForm, UpdateCartItemForm
from .models import Cart


class CartItemList(ListView):

    def get_queryset(self):
        return self.request.cart.items.all()

    def get_context_data(self, **kwargs):
        context = super(CartItemList, self).get_context_data(**kwargs)
        context.update({
            'available_object_list': [],
            'unavailable_object_list': [],
            'held_object_list': [],
        })
        for object in context['object_list']:
            if object.is_available:
                if object.is_held:
                    context['held_object_list'].append(object)
                else:
                    context['available_object_list'].append(object)
            else:
                context['unavailable_object_list'].append(object)
        return context

    def get(self, request, *args, **kwargs):
        return super(CartItemList, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CartItemForm(request.POST)
        if form.is_valid():
            form.add_to_cart(request.cart)
            if request.is_ajax():
                return HttpResponse(status=201)
            return redirect('tinycart_cart_item_list')
        return HttpResponseBadRequest()


class CartItemDetail(SingleObjectMixin, View):

    def get_queryset(self):
        return self.request.cart.items.all()

    def put(self, request, *args, **kwargs):
        form = UpdateCartItemForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return HttpResponse(status=200)
            return redirect('tinycart_cart_item_list')
        return HttpResponseBadRequest()

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        if request.is_ajax():
            return HttpResponse(status=204)
        return redirect('tinycart_cart_item_list')
