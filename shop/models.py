# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from users.models import CustomUser


class Category(models.Model):
    """Категории, к которым относятся товары"""
    name = models.CharField(max_length=150, db_index=True, verbose_name='Название категории', unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Subcategory(models.Model):
    """Подкатегории, к которым относятся товары"""
    category = models.ForeignKey(Category, related_name='subcategory', on_delete=models.CASCADE,
                                 verbose_name='Выберите категорию',
                                 )
    name = models.CharField(max_length=150, db_index=True, verbose_name='Название подкатегории')
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'подкатегория'
        verbose_name_plural = 'подкатегории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_subcategory', args=[self.slug])


class Product(models.Model):
    """Модель описания продукта"""
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE,
                                    verbose_name='Выберите подкатегорию'
                                    )

    article = models.IntegerField()
    aID = models.CharField(max_length=100, blank=True, null=True, verbose_name='aID')
    slug = models.SlugField(max_length=200, db_index=True)

    name = models.CharField(max_length=200, db_index=True, verbose_name='Наменование')
    description = models.TextField(blank=True, verbose_name='Описание')
    producer = models.TextField(blank=True, verbose_name='Производитель')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Цена')

    available = models.BooleanField(default=False, verbose_name='Наличие')
    size = models.CharField(max_length=15, blank=True, verbose_name='Размер')
    color = models.CharField(max_length=100, blank=True, verbose_name='Цвет')
    material = models.CharField(max_length=100, blank=True, verbose_name='Материал')

    image150x150 = models.URLField(blank=True, null=True, verbose_name='Фото150x150')
    image1 = models.URLField(blank=True, null=True, verbose_name='Фото1')
    image2 = models.URLField(blank=True, null=True, verbose_name='Фото2')
    image3 = models.URLField(blank=True, null=True, verbose_name='Фото3')
    image4 = models.URLField(blank=True, null=True, verbose_name='Фото4')
    image5 = models.URLField(blank=True, null=True, verbose_name='Фото5')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Order(models.Model):
    CART = '1_cart'
    WAIT = '2_wait'
    PAID = '3_paid'
    STATUS_CHOICES = [
        (CART, 'cart'),
        (WAIT, 'wait'),
        (PAID, 'paid'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=CART)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('status',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.user} - {self.status}'

    @staticmethod
    def get_cart(user: CustomUser):
        cart = Order.objects.filter(
            user=user,
            status=Order.CART
        ).first()

        if not cart:
            cart = Order.objects.create(
                user=user,
                status=Order.CART,
                amount=0,
            )
        return cart

    def get_amount(self):
        amount = Decimal(0)
        for item in self.orderitem_set.all():
            amount += item.amount
        return amount

    def make_order(self):
        item = self.orderitem_set.all()

        if item and self.status == Order.CART:
            self.status = Order.WAIT
            self.save()

    @staticmethod
    def get_amount_of_unpaid(user: CustomUser):
        amount = Order.objects.filter(user=user,
                                      status=Order.WAIT
                                      ).aggregate(Sum('amount'))['amount__sum']
        return amount or Decimal(0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    @property
    def amount(self):
        return self.quantity * self.price


@receiver(post_save, sender=OrderItem)
def recalculation_save(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


@receiver(post_delete, sender=OrderItem)
def recalculation_delete(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()





