import pymysql

conn = pymysql.connect(
    host="localhost", user="root", password="mariadb", db="mytrading", port=3306, charset="utf8"
)

cursor = conn.cursor()
cursor.execute("select version();")
result = cursor.fetchone()

print(f"MariaDB version : {result}")

conn.close()
