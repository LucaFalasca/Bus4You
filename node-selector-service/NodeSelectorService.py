import json

import pika

import OrsDao
from Neo4jDAO import *
import threading
import xmlrpc.server
import datetime

MAKE_ROUTE_STOP_DATA_QUEUE_1 = 'make_route_stop_data_1'
queue_channel = None

'''Funzione per inizializzare le code di rabbitMq e ricevere l'handler per la comunicazione, per aggiungere una coda
basta aggiungere un'altra queue declare con il nome della coda che si vuole creare che deve essere univoco, ricordare
che se si hanno più consumer per lo stesso messaggio occorre creare una coda per consumer in quanto un messaggio
può essere consumato una sola volta, sulla quale poi si pubblicheranno gli stessi messaggi'''


def init_rabbit_mq_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitMq', heartbeat=3600,
                                                                   blocked_connection_timeout=3600))
    channel = connection.channel()
    channel.queue_declare(queue=MAKE_ROUTE_STOP_DATA_QUEUE_1, durable=True)
    return channel


'''Funzione per pubblicare su una coda di rabbit_mq, necessita del channel ricevuto tramite la init, la coda su cui 
si vuole pubblicare e il messaggio da pubblicare, il messaggio deve essere un json che contiene le info necessarie
'''


def publish_message_on_queue(message_json, queue, channel):
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message_json.encode('utf-8'),
                          properties=pika.BasicProperties(delivery_mode=2))
    print("Sent message on queue:" + queue)
    print(message_json)


def send_nodes_for_computation(id):
    print("Inizio elaborazione")
    l = 0
    print("-id scelto: " + str(id))
    nodes_4j = get_cluster_with_limits(id, 10)
    print("Fatto!")
    l = len(nodes_4j)
    print("numero nodi presi" + str(l))
    print(nodes_4j)
    if l >= 7:  # min
        delete_nodes_after_get_cluster(nodes_4j)
        print("Ho scelto i nodi:")
        print(nodes_4j)
        # nodes_4j = get_cluster_with_limits(15, 3)

        # print(nodes_4j)

        node_limit = {}
        points_location = {}
        prec_hash = {}
        user_routes = []

        c = 0

        for itinerario in nodes_4j:
            print("ciclo")
            it_id = itinerario["it_id"]
            print("ciclo1")
            date = itinerario["date"]
            print("ciclo2")
            coord_start = [itinerario["position_start_stop"][0], itinerario["position_start_stop"][1]]
            print("ciclo3")
            # print(coord_start)
            if itinerario["hour"][0] is not None:
                print("ciclo4")
                print(itinerario["hour"][0])
                time = datetime.datetime.strptime(itinerario["hour"][0], '%H:%M').time()
                print(time)
                limit0 = time.hour * 60 + time.minute
            else:
                limit0 = None
            if itinerario["hour"][1] is not None:
                print("ciclo5")
                time = datetime.datetime.strptime(itinerario["hour"][1], '%H:%M').time()
                limit1 = time.hour * 60 + time.minute
            else:
                limit1 = None
            limit = [limit0, limit1]
            print("ciclo6")

            if coord_start not in points_location.values():
                k_start = c
                points_location[str(k_start)] = coord_start
                c += 1
                print("ciclo7")
            else:
                for key, value in points_location.items():
                    if value == coord_start:
                        print("ciclo7.5")
                        k_start = key
                        points_location[str(k_start)] = coord_start
                        break
            print("ciclo8")
            coord_end = [itinerario["position_end_stop"][0], itinerario["position_end_stop"][1]]
            # print(coord_end)
            if coord_end not in points_location.values():
                print("ciclo9")
                k_end = c
                points_location[str(k_end)] = coord_end
                c += 1
            else:
                for key, value in points_location.items():
                    if value == coord_end:
                        k_end = key
                        points_location[str(k_end)] = coord_end
                        break
            print("ciclo10")
            if str(k_start) not in prec_hash.keys():
                prec_hash[str(k_start)] = [str(k_end)]
            else:
                prec_hash[str(k_start)].append(str(k_end))
            if str(k_end) not in prec_hash.keys():
                prec_hash[str(k_end)] = []
            
            print("ciclo11")
            if limit is not None:
                if limit[0] is not None:
                    if str(k_start) not in node_limit.keys():
                        node_limit[str(k_start)] = [limit[0], None]
                    else:
                        if node_limit[str(k_start)][0] is None:
                            node_limit[str(k_start)][0] = limit[0]
                        else:
                            node_limit[str(k_start)][0] = min(node_limit[str(k_start)][0], limit[0])
                if limit[1] is not None:
                    if str(k_end) not in node_limit.keys():
                        node_limit[str(k_end)] = [None, limit[1]]
                    else:
                        if node_limit[str(k_end)][1] is None:
                            node_limit[str(k_end)][1] = limit[1]
                        else:
                            node_limit[str(k_end)][1] = max(node_limit[str(k_end)][1], limit[1])
            print("ciclo12")
            user_routes.append({
                "user": itinerario["user"],
                "it_id": it_id,
                "date": str(date),
                "nodes": [str(k_start), str(k_end)]
            })
            print("ciclo13")

        # print(points_location)
        # print(prec_hash)
        # print(node_limit)
        # print(user_routes)

        input_ors = [q[::-1] for q in list(points_location.values())]
        dist_matrix = OrsDao.getMatrix(input_ors)
        message = {"node_limit": node_limit, "prec_hash": prec_hash, "dist_matrix": dist_matrix,
                   "user_routes": user_routes, "points_location": points_location}
        print("Sending message: " + str(message))
        publish_message_on_queue(json.dumps(message), MAKE_ROUTE_STOP_DATA_QUEUE_1, queue_channel)
    print("Fine elaborazione")
    return 0


def get_booking_from_db():
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    return dao.get_all_bookings()


def get_cluster_with_limits(booking_id, limit):
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    return dao.get_start_end_bookings_with_limit(booking_id, limit)


def get_random_cluster_with_limits(limit):
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    booking_id = dao.get_random_booking()
    print("Booking id pescato:")
    print(booking_id)
    return dao.get_start_end_bookings_with_limit(booking_id, limit)


def get_cluster_with_limits_stripped(booking_id, limit):
    dao = Neo4jDAO("neo4j://localhost:7687", "neo4j", "123456789")
    ret = []
    nodes = dao.get_start_end_bookings_with_limit(booking_id, limit)
    dao.close()
    for elem in nodes:
        tmp_date = elem['date']
        elem['date'] = tmp_date.strftime("%Y-%m-%d")
        tmp_time = elem['hour']
        elem['hour'] = tmp_time[0].strftime("%H:%M")
        tmp_start_point = elem['position_start_stop']
        tmp_end_point = elem['position_end_stop']
        elem['position_start_stop'] = [tmp_start_point.latitude, tmp_start_point.longitude]
        elem['position_end_stop'] = [tmp_end_point.latitude, tmp_end_point.longitude]
        ret.append(elem)
    return ret


def get_random_cluster_with_limits_stripped(limit):
    dao = Neo4jDAO("neo4j://localhost:7687", "neo4j", "123456789")
    booking_id = dao.get_random_booking_it_id()
    ret = []
    print("Booking id pescato:")
    print(booking_id)
    nodes = dao.get_start_end_bookings_with_limit(booking_id, limit)
    dao.close()
    for elem in nodes:
        tmp_date = elem['date']
        elem['date'] = tmp_date.strftime("%Y-%m-%d")
        tmp_time = elem['hour']
        elem['hour'] = tmp_time[0].strftime("%H:%M")
        tmp_start_point = elem['position_start_stop']
        tmp_end_point = elem['position_end_stop']
        elem['position_start_stop'] = [tmp_start_point.latitude, tmp_start_point.longitude]
        elem['position_end_stop'] = [tmp_end_point.latitude, tmp_end_point.longitude]
        ret.append(elem)
    return ret


def delete_nodes_from_list(list):
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    dao.delete_nodes_from_list(list)
    dao.close()


def delete_nodes_after_get_cluster(list):
    ids = [d["id"] for d in list]
    print("Ecco la lista: ")
    print(ids)
    delete_nodes_from_list(ids)


def serverRPCThread():
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Server RPC is ON on port 8000")

    server.register_function(send_nodes_for_computation, "send_nodes_for_computation")
    server.register_function(get_random_cluster_from_it_id, "get_random_cluster_from_it_id")
    server.register_function(get_all_clusters, "get_all_clusters")
    server.register_function(get_random_cluster, "get_random_cluster")  # Registra il metodo get_random_cluster
    server.serve_forever()


def get_random_cluster_from_it_id(it_id):
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    ret = dao.get_cluster_nodes_json(int(it_id))
    dao.close()
    return ret


def get_all_clusters():
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    ret = dao.get_all_clusters_json()
    dao.close()
    return ret


def get_random_cluster():
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    ret = dao.get_random_cluster_json()
    print(ret)
    dao.close()
    return ret


if __name__ == "__main__":
    # create queues for rabbitMq the channel has to be passed as parameter to publish function
    # print(get_random_cluster_with_limits(10))
    queue_channel = init_rabbit_mq_queues()  # queue_connection va ammmazzata quando non serve piu
    # send_nodes_for_computation(queue_channel)
    # while True:
    #    pass

    serverRPCThread = threading.Thread(target=serverRPCThread)
    serverRPCThread.start()
    serverRPCThread.join()
