from datetime import datetime

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
            # print(len(res))
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
                # Create a cursor object to execute queries

                # Create the trigger SQL statement
                trigger_sql = "CREATE EVENT scadenza_route_" + str(route_id) + " ON SCHEDULE AT '" \
                              + route_expiration + "' DO call scadenza(" + str(route_id) + ");"
                print(trigger_sql)
                # Execute the trigger SQL statement
                curs.execute(trigger_sql)

                # insert order list
                print("Inserisco gli ordini")
                c = 1
                for order in order_list:
                    args = (c, route_id, order[1], order[2])
                    c += 1
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

    @staticmethod
    def retry_info_query(conn, it_id):
        ret = []
        res = None
        if conn is not None:
            print("Connection with db successful")
            print("it_id: ", it_id)
            curs = conn.cursor()
            args = (it_id,)
            curs.callproc('get_it_req_info_with_it_prop_id', args)
            conn.commit()
            for result in curs.stored_results():
                res = result.fetchall()
            curs.close()
            for elem in res:
                '''
                it_req_id, it_req_ora_inizio, it_req_ora_fine, it_req_costo_max, it_req_distanza, utente,
                it_req_fermata_lat_partenza, it_req_fermata_lon_partenza, it_req_fermata_lat_arrivo, 
                it_req_fermata_lon_arrivo, nome fermata partenza, nome fermata arrivo
                '''
                ret.append([elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], elem[8], elem[9], elem[10],
                            elem[11]])
            return ret
        else:
            print("Connection with db failed")
            return -1


    @staticmethod
    def get_stops_from_it_query(conn, it):
        ret = []
        res = None
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            curs.callproc('get_stops_from_it', (it,))
            conn.commit()
            for result in curs.stored_results():
                res = result.fetchall()
            curs.close()
            for elem in res:
                ret.append([elem[0], elem[1], elem[2]])
            print(ret)
            return ret
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def insert_it_req(conn, orario, costo_max, mail, fermata_lat_partenza, fermata_lon_partenza,
                      fermata_lat_arrivo, fermata_lon_arrivo, is_start_hour):
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()

            # insert request it
            args = (orario, costo_max, mail, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo,
                    fermata_lon_arrivo, is_start_hour)
            curs.callproc('insert_it_req', args)
            res = None
            # get output parameter value which is the auto incremental generated route id
            for result in curs.stored_results():
                res = result.fetchall()
            req_id = res[0][0]
            print("Returned route id: ", req_id)
            conn.commit()
            return req_id
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def get_user_balance(conn, mail):
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()

            # get balance
            args = (mail, )
            curs.callproc('get_user_balance', args)
            res = None

            for result in curs.stored_results():
                res = result.fetchall()
            balance = res[0][0]
            conn.commit()
            return balance
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def get_future_confirmed_routes_query(conn):
        ret = []
        res = None
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            curs.callproc('get_future_confirmed_routes')
            conn.commit()
            for result in curs.stored_results():
                res = result.fetchall()
            curs.close()
            for elem in res:
                ret.append([elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]])
            return ret
        else:
            print("Connection with db failed")
            return -1

    @staticmethod
    def get_stop_name_from_coords(conn, lat, lon):
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()

            # get balance
            args = (lat, lon)
            curs.callproc('get_stop_name_from_coordinates', args)
            res = None

            for result in curs.stored_results():
                res = result.fetchall()
            stop_name = res[0][0]
            conn.commit()
            return stop_name
        else:
            print("Connection with db failed")
            return -1


    @staticmethod
    def get_total_km_query(conn, route_id):
        if conn is not None:
            print("Connection with db successful")
            curs = conn.cursor()
            ret = []

            # get balance
            args = (route_id, )
            curs.callproc('get_route_distance', args)
            res = None
            conn.commit()
            for result in curs.stored_results():
                res = result.fetchall()
            curs.close()
            for elem in res:
                ret.append([elem[0], elem[1]])
            
            return ret
            
            return km
        else:
            print("Connection with db failed")
            return -1