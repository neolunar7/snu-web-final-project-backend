import pymysql


# Database
host = "0.0.0.0"
port = 3306
user = "root"
password = "mysql"
database = "snu"


def get_conn() -> pymysql.Connection:
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )
