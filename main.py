import sqlite3
import random

# Подключаемся к файлу базы данных:
conn = sqlite3.connect('shop.sqlite')
cur = conn.cursor()

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
print("Join:")
cur.execute('SELECT u.first_name, u.last_name, ubo.id, bi.item_id FROM User AS u LEFT JOIN UserBasketOrder AS ubo ON u.id = ubo.user_id INNER JOIN BasketItems AS bi ON ubo.id = bi.basket_id')
for row in cur:
    print(row)
cur.close()
