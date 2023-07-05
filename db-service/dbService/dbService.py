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


if __name__ == "__main__":
    serve()
