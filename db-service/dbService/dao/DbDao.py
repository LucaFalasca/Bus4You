import mysql.connector
from mysql.connector import Error


class DbDao:
    def __init__(self):
        self.db_ip = 'mysqlDb'  # For docker if the db is deployed in a container
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
    def stop_query(conn):
        ret = []
        res = None
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            curs.callproc('get_stops')
            conn.commit()
            for result in curs.stored_results():
                res = result.fetchall()
            curs.close()
            for elem in res:
                ret.append([elem[0], elem[1], elem[2]])
            return ret
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def user_routes_query(conn, usr):
        ret = []
        res = None
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            curs.callproc('get_user_routes', (usr,))
            conn.commit()
            for result in curs.stored_results():
                res = result.fetchall()
            curs.close()
            print(len(res))
            for elem in res:
                '''
                costo, orario partenza proposto, orario arrivo proposto, stato itinerario proposto, flag percorso passato,
                stato percorso, scadenza, nome fermata partenza, nome fermata arrivo
                '''
                ret.append([elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], elem[8], elem[9]])
            print(ret)
            return ret
        else:
            print("Connection with db failed")
            return -1
