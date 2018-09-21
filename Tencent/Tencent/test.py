import pymysql
# with pymysql.connect(host='192.168.200.31', user='root', passwd="123456", db='bus') as conn:
#     conn.execute("SELECT * FROM test0000")
#     for r in conn:
#         print(r)
with pymysql.connect(host='192.168.200.31', user='root', passwd="123456", db='bus') as conn:
    conn.execute("create table Station(")