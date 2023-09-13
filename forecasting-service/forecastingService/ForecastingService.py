import xmlrpc.server


def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    #server.register_function(get_stops, "get_stops")
    server.serve_forever()


if __name__ == "__main__":
    serve()