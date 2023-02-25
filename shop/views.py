# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, DeleteView
from shop.models import Product, Order, OrderItem
from shop.forms import AddQuantityForm


class ProductsListView(ListView):
    paginate_by = 24
    model = Product
    template_name = 'shop/shop.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        query_subcategory = self.request.GET.get('subcategory')

        if not query:
            query = ""

        object_list = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

        if not query_subcategory:
            query_subcategory = ''

        else:
            object_list = Product.objects.filter(
               Q(subcategory__name__icontains=query_subcategory)
            )

        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        search_q = self.request.GET.get('search')
        category_q = self.request.GET.get('subcategory')

        if category_q is None:
            category_q = ''

        if search_q is None:
            search_q = ''
        context['search'] = search_q
        context['subcategory'] = category_q

        return context


class ProductsDetailView(DetailView):
    model = Product
    template_name = 'shop/product.html'


@login_required(login_url=reverse_lazy('login'))
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantityForm(request.POST)
        print(quantity_form['quantity'])
        if quantity_form.is_valid():
            print('1')
            quantity = quantity_form.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(request.user)
                product = get_object_or_404(Product, pk=pk)
                cart.orderitem_set.create(product=product,
                                          quantity=quantity,
                                          price=product.price)
                cart.save()
                return redirect('cart_view')
        else:
            pass
    return redirect('shop')


@login_required(login_url=reverse_lazy('login'))
def cart_view(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'shop/cart.html', context)


@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'shop/cart.html'
    success_url = reverse_lazy('cart_view')

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs
