import mysql.connector
from mysql.connector import Error


class DbDao:
    def __init__(self):
        self.db_ip = 'mysqlDb'  # For docker if the db is deployed in a container
        # self.db_ip = 'host.docker.internal'  # For docker if the db is deployed in the docker container host
        # self.db_ip = 'localhost'
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
    def stop_query_rect(conn, x, y, height, width):
        ret = []
        res = None
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            curs.callproc('get_stops_rect', (x, y, height, width))
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
                stato percorso, scadenza, nome fermata partenza, nome fermata arrivo, id itinerario
                '''
                ret.append([elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], elem[8], elem[9]])
            return ret
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def confirm_it(conn, it_id):
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            args = (it_id,)
            curs.callproc('confirm_it', args)
            conn.commit()
            curs.close()
            return 0
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def reject_it(conn, it_id):
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            args = (it_id,)
            curs.callproc('reject_it', args)
            conn.commit()
            curs.close()
            return 0
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def insert_route_info(conn, route_expiration, order_list, it_list):
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            try:
                conn.autocommit = False
                conn.start_transaction(consistent_snapshot=True,
                                       isolation_level='REPEATABLE READ',
                                       readonly=False)
                # insert route
                print("Inserisco il percorso")
                args = (route_expiration,)
                curs.callproc('insert_route', args)
                res = None
                # get output parameter value which is the auto incremental generated route id
                for result in curs.stored_results():
                    res = result.fetchall()
                route_id = res[0][0]
                print("Returned route id: ", route_id)

                # insert order list
                print("Inserisco gli ordini")
                for order in order_list:
                    args = (order[0], route_id, order[1], order[2])
                    print(args)
                    curs.callproc('insert_order', args)

                print("Inserisco gli itinerari")
                # insert itinerary list
                for it in it_list:
                    args = (it[0], it[1], it[2], it[3], it[4], it[5], route_id, it[6], it[7], it[8], it[9])
                    curs.callproc('insert_it_proposed', args)

                conn.commit()
                return 0

            except mysql.connector.Error as error:
                # rollback transaction on error
                print("Error occurred: {}".format(error))
                conn.rollback()
                return -2

            finally:
                # close cursor and connection
                curs.close()
        else:
            print("Connection with db failed")
            return -1
