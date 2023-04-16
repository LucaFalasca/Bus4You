import mysql.connector
from mysql.connector import Error


class UserDbDao:
    def __init__(self, db_ip, db_name, usr, pwd):
        self.db_ip = db_ip
        self.db_name = db_name
        self.usr = usr
        self.pwd = pwd

    def connect(self):
        try:
            connection = mysql.connector.connect(host=self.db_ip,
                                                 database=self.db_name,
                                                 user=self.usr,
                                                 password=self.pwd)
            if connection.is_connected():
                return connection

        except Error as e:
            print("Error while connecting to MySQL", e)
            return None
