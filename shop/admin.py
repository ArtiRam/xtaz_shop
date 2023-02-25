# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from shop.models import Product, Category, Subcategory, Order, OrderItem, Payment

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
