import mysql.connector

config = {
    "host" : "f1_mysql",
    "user" : "root",
    "port" : "3306",
    "password" : "root",
    "database" : "f1db",
    "raise_on_warnings": True
}


def get_connection():
    return mysql.connector.connect(**config)
