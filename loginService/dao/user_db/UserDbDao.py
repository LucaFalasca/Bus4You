import mysql.connector
from mysql.connector import Error


class UserDbDao:
    def __init__(self, db_ip, db_name, usr, pwd):
        self.db_ip = 'host.docker.internal'
        self.db_name = 'b4y_userdb'
        self.usr = 'root'
        self.pwd = 'root'

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
