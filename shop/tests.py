# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import pandas as pd
import csv
from shop.models import Category, Subcategory, Product
from django.db.utils import IntegrityError

df = pd.read_csv('sheet.csv', sep=';', skiprows=1)
df.to_csv('sheet.csv', index=False)

with open('sheet.csv', 'r', encoding="utf8") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')

    for row in reader:
        # 0 - артикул
        # 1 - категория
        # 2 - подкатегория
        # 3 - name
        # 4 - Описание
        # 5 - Производитель
        # 6 - Артикул производителя
        # 7 - Цена (Розница)
        # 8 - Цена (Опт)
        # 9 - Можно купить(1, 0)
        # 10 - На складе
        # 11 - Время отгрузки(1, 2, 3)
        # 12 - Размер
        # 13 - Цвет
        # 14 - aID
        # 15 - Материал
        # 16 - Батарейки
        # 17 - Упаковка
        # 18 - Вес (брутто)
        # 19 - Фотография маленькая до 150*150
        # 20-24 - Фотография 1-4
        # 25 - Штрихкод
        try:
            if Category.objects.filter(name=row[1]).exists():
                if Subcategory.objects.filter(name=row[2]).exists():
                    if Product.objects.filter(name=row[3]).exists():
                        pass
                    else:
                        subcategory = Subcategory.objects.get(name=row[2])

                        product = Product(article=row[0], aID=row[14], slug=row[3], subcategory=subcategory,

                                          name=row[3], description=row[4], producer=row[5], price=row[7],

                                          available=row[9], size=row[12], color=row[13], material=row[15],

                                          image150x150=row[19], image1=row[20], image2=row[21],
                                          image3=row[22], image4=row[23], image5=row[24]
                                          )
                        product.save()

                category = Category.objects.get(name=row[1])
                subcategory = Subcategory(category=category, name=row[2], slug=row[2])
                product = Product(article=row[0], aID=row[14], slug=row[3], subcategory=subcategory,

                                  name=row[3], description=row[4], producer=row[5], price=row[7],

                                  available=row[9], size=row[12], color=row[13], material=row[15],

                                  image150x150=row[19], image1=row[20], image2=row[21],
                                  image3=row[22], image4=row[23], image5=row[24]
                                  )

                subcategory.save()
                product.save()

            category = Category(name=row[1], slug=row[1])
            category.save()

            subcategory = Subcategory(category=category, name=row[2], slug=row[2])
            subcategory.save()

            product = Product(article=row[0], aID=row[14], slug=row[3], subcategory=subcategory,

                              name=row[3], description=row[4], producer=row[5], price=row[7],

                              available=row[9], size=row[12], color=row[13], material=row[15],

                              image150x150=row[19], image1=row[20], image2=row[21],
                              image3=row[22], image4=row[23], image5=row[24]
                              )
            product.save()

        except IntegrityError:
            pass
