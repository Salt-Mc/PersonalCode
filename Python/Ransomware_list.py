import pyodbc

db_file = r'''ransom_list.ac'''
user = ''
password = ''

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb)};'
    r'DBQ=ransom_list.mdb;')
conn = pyodbc.connect(conn_str)
cur = conn.cursor()

dt = str(input("Date :"))
name = input("Name: ")
url = str(input("Url: "))

cur.execute(u"""INSERT INTO Ransomware_list VALUES ({},{},{})""".format(dt, name, url))
cur.commit()
cur.close()
