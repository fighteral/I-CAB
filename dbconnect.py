import MySQLdb
def connection():
    conn=MySQLdb.connect("localhost","root","","icab")
    c=conn.cursor()
    return c,conn
