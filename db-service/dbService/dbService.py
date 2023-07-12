from flask import json
import xmlrpc.server
from dao.DbDao import DbDao


def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    server.register_function(get_stops, "get_stops")
    server.register_function(get_user_routes, "get_user_routes")
    server.register_function(get_stops_rect, "get_stops_rect")
    server.register_function(confirm_it, "confirm_it")
    server.register_function(reject_it, "reject_it")
    server.register_function(insert_route_info, "insert_route_info")
    server.register_function(get_retry_info, "get_retry_info")
    server.register_function(get_stops_from_it, "get_stops_from_it")
    server.register_function(insert_it_req, "insert_it_req")
    server.serve_forever()


def get_stops():
    usr_db = DbDao()
    conn = usr_db.connect()
    stop_list = usr_db.stop_query(conn)
    conn.close()
    return json.dumps(stop_list)


def get_stops_rect(x, y, height, width):
    usr_db = DbDao()
    conn = usr_db.connect()
    stop_list = usr_db.stop_query_rect(conn, x, y, height, width)
    conn.close()
    return json.dumps(stop_list)


def get_user_routes(mail):
    usr_db = DbDao()
    conn = usr_db.connect()
    routes_list = usr_db.user_routes_query(conn, mail)
    conn.close()
    return json.dumps(routes_list)


def confirm_it(it_id):
    usr_db = DbDao()
    conn = usr_db.connect()
    ret = usr_db.confirm_it(conn, it_id)
    conn.close()
    if ret == 0:
        return {"status": "ok"}
    else:
        return {"status": "error"}


def reject_it(it_id):
    usr_db = DbDao()
    conn = usr_db.connect()
    ret = usr_db.reject_it(conn, it_id)
    conn.close()
    if ret == 0:
        return {"status": "ok"}
    else:
        return {"status": "error"}

'''
route_expiration(DATETIME) è la data di scadenza del percorso

order_list è una lista di liste, e contiene le informazioni per popolare le relazioni "ordinamento" cioè quelle che ci 
dicono l'ordine delle fermate all'interno del percorso, la lista è fatta come segue:
[[numero(INT), stop_latitude(DECIMAL(8,6)), stop_longitude(DECIMAL(8,6))], ...] -> numero è la posizione della fermata 
nel percorso e.g la fermata x è la seconda fermata del percorso, DECIMAL(8,6) significa 8 cifre di cui 6 decimali quindi
2 intere e 6 decimali.

it_list è una lista di liste, e contiene le informazioni per popolare itinerario_proposto, è fatta come segue
[[costo_€(DECIMAL(6,2)), distanza_km(DECIMAL(8,4)), orario_partenza_proposto(DATETIME), 
orario_arrivo_proposto(DATETIME), mail_utente(VARCHAR(128)), id_itinerario_richiesto(BIGINT), 
fermata_lat_partenza(DECIMAL(8,6)), fermata_lon_partenza(DECIMAL(8,6)), fermata_lat_arrivo(DECIMAL(8,6)), 
fermata_lon_arrivo(DECIMAL(8,6))], ...] -> id_itinerario_richiesto va preso dal db precedentemente
'''
def insert_route_info(route_expiration, order_list, it_list):
    usr_db = DbDao()
    conn = usr_db.connect()
    ret = usr_db.insert_route_info(conn, route_expiration, order_list, it_list)
    conn.close()
    if ret == 0:
        return {"status": "ok"}
    else:
        return {"status": "error"}


def get_retry_info(it_id):
    usr_db = DbDao()
    conn = usr_db.connect()
    it_req_info = usr_db.retry_info_query(conn, it_id)
    conn.close()
    return json.dumps(it_req_info)

def get_stops_from_it(it_id):
    print("HEYLA")
    usr_db = DbDao()
    conn = usr_db.connect()
    stops = usr_db.get_stops_from_it_query(conn, it_id)
    conn.close()
    print(stops)
    return json.dumps(stops)

'''
Query per inserire su db un itinerario richiesto, ritorna l'id autoincrementale generato dalla insert
orario(DATETIME), costo_max(DECIMAL(6,2)), mail_utente(VARCHAR(128)), fermata_lat_partenza(DECIMAL(8,6)),
fermata_lon_partenza(DECIMAL(8,6)), fermata_lat_arrivo(DECIMAL(8,6)), fermata_lon_arrivo(DECIMAL(8,6)), 
isStartHour(BOOLEAN) 0 se è orario di arrivo, 1 se è orario di partenza
'''
def insert_it_req(orario, costo_max, mail, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo,
                  fermata_lon_arrivo, is_start_hour):
    usr_db = DbDao()
    conn = usr_db.connect()
    it_req_info = usr_db.insert_it_req(conn, orario, costo_max, mail, fermata_lat_partenza, fermata_lon_partenza,
                                          fermata_lat_arrivo, fermata_lon_arrivo, is_start_hour)
    conn.close()
    return json.dumps(it_req_info)


if __name__ == "__main__":
    '''order_list = [[1, 41.648593, 12.431090], [2, 41.654548, 12.427688]]
    it_list = [[1.5, 5.52, "2023-05-05 12:00:00", "2023-05-05 12:30:00", "prova@gmail.com", 1, 41.648593, 12.431090,
                41.654548, 12.427688], [10.5, 20.52, "2023-05-05 12:00:00", "2023-05-05 12:30:00", "prova@gmail.com",
                                        2, 41.648593, 12.431090, 41.654548, 12.427688]]
    insert_route_info("2023-07-11 19:28:00", order_list, it_list)'''
    serve()


