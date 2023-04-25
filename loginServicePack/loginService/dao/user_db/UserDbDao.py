import mysql.connector
from mysql.connector import Error


class UserDbDao:
    def __init__(self):
        #self.db_ip = 'host.docker.internal' #For docker if the db is deployed in the docker container host
        self.db_ip = 'localhost'
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
            else:
                print("Error while connecting to MySQL")

        except Error as e:
            print("Error while connecting to MySQL", e)
            return None

    @staticmethod
    def login_query(conn, mail, password):
        res = None
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            args = (mail, password)
            print(args)
            curs.callproc('login', args)
            for result in curs.stored_results():
                res = result.fetchall()
            curs.close()
            # Check result
            if res[0][0] == 1:
                return 0
            else:
                return 1
        else:
            print("Connection with db failed")
            return -1
