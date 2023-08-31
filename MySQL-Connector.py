import datetime
import mysql.connector

cnx = mysql.connector.connect(user='vsc', password='blaster123',
                              host='127.0.0.1',
                              database='stock')
cursor = cnx.cursor()

query = ("SELECT p.date AS 'date', p.Symbol AS 'symbol', p.close AS 'close' FROM price_quotes AS p "
         "WHERE p.date BETWEEN %s AND %s")

date_start = datetime.date(2022, 1, 1)
date_end = datetime.date(2022, 1, 9)

cursor.execute(query, (date_start, date_end))

for (date, symbol, close) in cursor:
  print("{}, {} closed {}".format(
    date, symbol, close))





cursor.close()
cnx.close()
