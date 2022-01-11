import pymysql
def cursor_connect():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           passwd='root',
                           db='test1'
    )
    cursor = conn.cursor()
    '''conn = pymysql.connect(host='localhost',
                       user='root',
                       passwd='asbZ5ayJ7W2',
                       db='test'
                        )
    cursor = conn.cursor()'''
    return [cursor, conn]

