from flask import json
import xmlrpc.server
from dao.DbDao import DbDao


def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    server.register_function(get_stops, "get_stops")
    server.register_function(get_user_routes, "get_user_routes")
    server.serve_forever()


def get_stops():
    usr_db = DbDao()
    conn = usr_db.connect()
    stop_list = usr_db.stop_query(conn)
    conn.close()
    return json.dumps(stop_list)


def get_user_routes(mail):
    usr_db = DbDao()
    conn = usr_db.connect()
    routes_list = usr_db.user_routes_query(conn, mail)
    conn.close()
    return json.dumps(routes_list)


if __name__ == "__main__":
    serve()
