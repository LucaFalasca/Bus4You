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


def test_rabbitMq(channel):
    node_limit = {'1': (None, 40),
                  '2': (80, None),
                  '4': (70, None)}
    prec_hash = {'0': ['1'], '1': [], '2': ['3'], '3': [], '4': ['5'], '5': []}
    #dist_matrix = [[0, 20, 10, 30, 20, 30],
    #               [20, 0, 10, 20, 10, 20],
    #               [10, 10, 0, 20, 10, 20],
    #               [30, 20, 20, 0, 10, 10],
    #               [20, 10, 10, 10, 0, 10],
    #               [30, 20, 20, 10, 10, 0]]
    user_routes = {"Giovanni": ('0', '1'),
                   "Marco": ('2', '3'),
                   "Luca": ('4', '5')}
    points_location = {'0' :[12.527504,41.837339],
                        '1' :[12.627504,41.837339],
                        '2' :[12.427504,41.837339],
                        '3' :[12.527504,41.737339],
                        '4' :[12.547504,41.737339],
                        '5' :[12.327504,41.767339]}
                       


    dist_matrix = OrsDao.getMatrix([[12.527504,41.837339],[12.627504,41.837339],[12.427504,41.837339],[12.527504,41.737339], [12.547504,41.737339], [12.327504,41.767339]])
    #message = [
    #    {"prova": "prova1"},
    #]
    message = {}
    message["node_limit"] = node_limit
    message["prec_hash"] = prec_hash
    message["dist_matrix"] = dist_matrix
    message["user_routes"] = user_routes
    message["date"] = "05/07/2023"
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
    print(get_random_cluster_with_limits(5))
    queue_channel = init_rabbit_mq_queues()  # queue_connection va ammmazzata quando non serve piu
    test_rabbitMq(queue_channel)
    #while True:
    #    pass
