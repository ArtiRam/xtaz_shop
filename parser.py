import csv
import pandas as pd




# df.column_name != whole string from the cell
# now, all the rows with the column: Name and Value: "dog" will be deleted

df = pd.read_csv('sheet.csv', sep=';', skiprows=1)
df.to_csv('sheet1.csv', index=False)

with open('sheet.csv', 'r', encoding="utf8") as csv_file:
    reader = csv.reader(csv_file, delimiter=';')

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
        print(row[0])

