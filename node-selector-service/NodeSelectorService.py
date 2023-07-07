import json
import pika
import OrsDao
import datetime
from Neo4jDAO import *




MAKE_ROUTE_STOP_DATA_QUEUE_1 = 'make_route_stop_data_1'


'''Funzione per inizializzare le code di rabbitMq e ricevere l'handler per la comunicazione, per aggiungere una coda
basta aggiungere un'altra queue declare con il nome della coda che si vuole creare che deve essere univoco, ricordare
che se si hanno più consumer per lo stesso messaggio occorre creare una coda per consumer in quanto un messaggio
può essere consumato una sola volta, sulla quale poi si pubblicheranno gli stessi messaggi'''
def init_rabbit_mq_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitMq'))
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
    print("Sent message" + message_json + "on queue: " + queue)


def send_nodes_for_computation(channel):
    l = 0
    while(l != 3):
        nodes_4j = get_random_cluster_with_limits(3)
        l = len(nodes_4j)
    print(nodes_4j)

    node_limit = {}
    points_location = {}
    prec_hash = {}
    user_routes = {}

    p = 1


    c = 0

    for itinerario in nodes_4j:
        date = itinerario["date"]
        coord_start = [itinerario["position_start_stop"][0], itinerario["position_start_stop"][1]]
        print(coord_start)
        if(itinerario["hour"][0] != None):
            limit0 = itinerario["hour"][0].hour * 60 + itinerario["hour"][0].minute
        else:
            limit0 = None
        if(itinerario["hour"][1] != None):
            limit1 = itinerario["hour"][1].hour * 60 + itinerario["hour"][1].minute
        else:
            limit1 = None
        limit = [limit0, limit1]

        if(coord_start not in points_location.values()):
            k_start = c
            points_location[str(k_start)] = coord_start
            c += 1
            
        else:
            for key, value in points_location.items():
                if(value == coord_start):
                    k_start = key
                    points_location[str(k_start)] = coord_start
                    break

        coord_end = [itinerario["position_end_stop"][0], itinerario["position_end_stop"][1]]
        print(coord_end)
        if(coord_end not in points_location.values()):
            k_end = c
            points_location[str(k_end)] = coord_end
            c += 1
        else:
            for key, value in points_location.items():
                if(value == coord_end):
                    k_end = key
                    points_location[str(k_end)] = coord_end
                    break
        if str(k_start) not in prec_hash.keys():
            prec_hash[str(k_start)] = [str(k_end)]
        else:
            prec_hash[str(k_start)].append(str(k_end))
        if str(k_end) not in prec_hash.keys():
            prec_hash[str(k_end)] = []
        
        if(limit != None):
            if(limit[0] != None):
                if(str(k_start) not in node_limit.keys()):
                    node_limit[str(k_start)] = [limit[0], None]
                else:
                    if node_limit[str(k_start)][0] == None:
                        node_limit[str(k_start)][0] = limit[0]
                    else:
                        node_limit[str(k_start)][0] = min(node_limit[str(k_start)][0], limit[0])
            if(limit[1] != None):
                if(str(k_end) not in node_limit.keys()):
                    node_limit[str(k_end)] = [None, limit[1]]
                else:
                    if node_limit[str(k_end)][1] == None:
                        node_limit[str(k_end)][1] = limit[1]
                    else:
                        node_limit[str(k_end)][1] = max(node_limit[str(k_end)][1], limit[1])
        
        user_routes["persona" + str(p)] = (str(k_start), str(k_end))
        p += 1
            

    print(points_location)
    print(prec_hash)
    print(node_limit)
    print(user_routes)
                       
    input_ors = [q[::-1] for q in list(points_location.values())]
    dist_matrix = OrsDao.getMatrix(input_ors)
    message = {}
    message["node_limit"] = node_limit
    message["prec_hash"] = prec_hash
    message["dist_matrix"] = dist_matrix
    message["user_routes"] = user_routes
    message["date"] = str(date)
    message["points_location"] = points_location
    publish_message_on_queue(json.dumps(message), MAKE_ROUTE_STOP_DATA_QUEUE_1, channel)


def get_booking_from_db():
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    return dao.get_all_bookings()

def get_cluster_with_limits(booking_id , limit):
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    return dao.get_start_end_bookings_with_limit(booking_id, limit)

def get_random_cluster_with_limits( limit):
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    booking_id = dao.get_random_booking()
    print(booking_id)
    return dao.get_start_end_bookings_with_limit(booking_id, limit)



if __name__ == "__main__":
    print("Hello World")
    #create queues for rabbitMq the channel has to be passed as parameter to publish function
    #print(get_random_cluster_with_limits(5))
    queue_channel = init_rabbit_mq_queues()  # queue_connection va ammmazzata quando non serve piu
    send_nodes_for_computation(queue_channel)
    #while True:
    #    pass
