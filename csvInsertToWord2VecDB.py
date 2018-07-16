# -*- coding: utf-8 -*-
import csv
import sqlite3
import sys


print("COLUM NUMBER MUST BE CHANGED IF IT's NOT 2")
print("DB NAME >")
dbName = raw_input()
print("CSV FILE NAME >")
csvName = raw_input()
print("TABLE NAME >")
tableName = raw_input()


conn = sqlite3.connect(dbName)
conn.text_factory = str
cur = conn.cursor()

with open('./csv/' + csvName , 'rb') as f: 
    b = csv.reader(f)
    header = next(b)
    for t in b:
	print(t)
        # tableに各行のデータを挿入する。
        cur.execute('INSERT INTO {0} VALUES (?,?);'.format(tableName), t)
	conn.commit()
