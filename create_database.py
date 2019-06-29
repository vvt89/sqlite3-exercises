import sqlite3
import random

# Список имен пользователей интернет-магазина
user_list = [['Svetlana', 'Ivanova'],
             ['Olga', 'Petrova'],
             ['Nikolay', 'Alexandrov'],
             ['Alexander', 'Nikolaev'],
             ['Roman', 'Bulkin'],
             ['Violetta', 'Durkina'],
             ['Stepan', 'Pichonin']]

# Список товаров
items_list = [['sclissors', 20, 'simple sclissors', 10],
              ['paper', 2, 'simple paper', 9],
              ['knife', 15, 'simple knife', 8],
              ['saw', 200, 'simple saw', 10],
              ['ham', 19, 'simple ham', 9],
              ['cheese', 13, 'simple cheese', 8],
              ['butter', 34, 'simple butter', 10],
              ['egg', 12, 'simple egg', 9]]

# Подключаемся к файлу базы данных и создаем курсор
conn = sqlite3.connect('shop.sqlite')
cur = conn.cursor()

# Создаем таблицы в базе данных, если они существуют, то удаляем
cur.execute('DROP TABLE IF EXISTS Sess')
cur.execute('CREATE TABLE Sess (id INTEGER, user_id INTEGER, sess TEXT)')
cur.execute('DROP TABLE IF EXISTS User')
cur.execute('CREATE TABLE User (id INTEGER, username TEXT, first_name TEXT, last_name TEXT, pass TEXT)')
cur.execute('DROP TABLE IF EXISTS UserBasketOrder')
cur.execute('CREATE TABLE UserBasketOrder (id INTEGER, user_id INTEGER, basket_id INTEGER)')
cur.execute('DROP TABLE IF EXISTS Items')
cur.execute('CREATE TABLE Items (id INTEGER, name TEXT, price INTEGER, description TEXT, rating INTEGER)')
cur.execute('DROP TABLE IF EXISTS Basket')
cur.execute('CREATE TABLE Basket (id INTEGER, user_id INTEGER)')
cur.execute('DROP TABLE IF EXISTS BasketItems')
cur.execute('CREATE TABLE BasketItems (id INTEGER, basket_id INTEGER, item_id INTEGER)')

# Заполняем таблицу с именами пользователей
for n,i in enumerate(user_list):
    params = (n, i[1]+str(n*n+1980), i[0], i[1], "123456")
    cur.execute('INSERT INTO User (id, username, first_name, last_name, pass) VALUES(?,?,?,?,?)', params)
conn.commit()

# Заполняем таблицу с наименованиями товаров
for n,i in enumerate(items_list):
    params = (n, i[0], i[1], i[2], i[3])
    cur.execute('INSERT INTO Items (id, name, price, description, rating) VALUES(?,?,?,?,?)', params)
conn.commit()

# Присваиваем пользователям по одной корзине
basket_ids = list(range(len(user_list)))
used_basket_ids = []
for i in range(len(user_list)-1):
    rand_id = random.choice(basket_ids)
    basket_ids.remove(rand_id)
    params = (i, i, rand_id)
    cur.execute('INSERT INTO UserBasketOrder (id, user_id, basket_id) VALUES(?,?,?)', params)
    used_basket_ids.append(rand_id)
conn.commit()

# Наполняем корзины покупателей товарами
probability_list = [0, 1, 2, 3]
item_ids = list(range(len(items_list)))
for i in range(len(user_list)):
    rand_num = random.choice(probability_list)
    for j in range(rand_num):
        rand_id = random.choice(item_ids)
        cur.execute('SELECT id FROM Items WHERE id = ?', (rand_id,))
        for n, row in enumerate(cur):
            if n == 0:
                item_id = row[0]
        params = (i, i, item_id)
        cur.execute('INSERT INTO BasketItems (id, basket_id, item_id) VALUES(?,?,?)', params)
conn.commit()

# Вывод полученных таблиц в консоль:
print("Users:")
cur.execute('SELECT * FROM User')
for row in cur:
    print(row)
print("Items:")
cur.execute('SELECT * FROM Items')
for row in cur:
    print(row)
print("UserBasketOrder:")
cur.execute('SELECT * FROM UserBasketOrder')
for row in cur:
    print(row)
print("BasketItems:")
cur.execute('SELECT * FROM BasketItems')
for row in cur:
    print(row)

#
cur.close()
