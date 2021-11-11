import pymysql
conn = pymysql.connect(host='localhost',
                       user='root',
                       passwd='root',
                       db='test1'
)
cursor = conn.cursor()

