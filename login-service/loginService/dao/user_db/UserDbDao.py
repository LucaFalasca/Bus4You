import mysql.connector
from mysql.connector import Error


class UserDbDao:
    def __init__(self):
        self.db_ip = 'mysqlDb' # For docker if the db is deployed in a container
        #self.db_ip = 'host.docker.internal'  # For docker if the db is deployed in the docker container host
        #self.db_ip = 'localhost'
        self.db_name = 'b4y_user_db'
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
        print("Sono nella funzione login_query della dao")
        res = None
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            args = (mail, password)
            curs.callproc('login', args)
            conn.commit()
            for result in curs.stored_results():
                res = result.fetchall()
            curs.close()
            # Check result
            if res[0][0] == 1:
                print("Login successful")
                return 0
            else:
                print("Login failed")
                return 1
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def sign_up(conn, name, surname, mail, password, birthdate, username): #Birthdate in format YYYY-MM-DD
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            args = (name, surname, mail, password, username, birthdate)
            curs.callproc('sign_up', args)
            conn.commit()
            curs.close()
            return 0
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def get_token(conn):
        res = None
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            try:
                curs.callproc('get_token')
                conn.commit()
                for result in curs.stored_results():
                    res = result.fetchall()
                return res[0][0]
            except mysql.connector.errors.DatabaseError as e:
                print("Error while calling get_token ", e)
                return None
            finally:
                curs.close()

        else:
            print("Connection with db failed")
            return None
