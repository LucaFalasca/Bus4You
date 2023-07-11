import json

import pika
import xmlrpc.server

from neo4j import GraphDatabase, basic_auth
from neo4j._spatial import WGS84Point
from Neo4jDAO_BS import *
from NodeToAlg import *
from Node import *
from utils import *
import threading
import datetime

PROPOSE_ROUTE_QUEUE = 'propose_route'

# Usare questa funzione per generare un insieme di prenotazioni con dati realistici
'''def generate_stops(sizeUsers):

    users = ["Marco", "Giulia", "Matteo", "Francesca", "Luca", "Chiara", "Alessandro", "Valentina", "Davide", "Sara",
            "Simone", "Martina", "Lorenzo", "Elisa", "Giacomo", "Federica", "Andrea", "Alice", "Giovanni", "Beatrice",
            "Nicola", "Elena", "Riccardo", "Cristina", "Stefano", "Maria", "Antonio", "Laura", "Filippo", "Caterina"]

    stops = [
        ["Termini", (41.9014, 12.5005)],
        ["Piazza Venezia", (41.8954, 12.4823)],
        ["Colosseo", (41.8902, 12.4923)],
        ["Circo Massimo", (41.8839, 12.4844)],
        ["Piazza Navona", (41.8992, 12.4736)],
        ["Campo de' Fiori", (41.8957, 12.4722)],
        ["Trastevere", (41.8896, 12.4673)],
        ["Piazza del Popolo", (41.9105, 12.4768)],
        ["Tiburtina", (41.9108, 12.5291)],
        ["San Giovanni", (41.8854, 12.5093)],
        ["Boccea", (41.9062, 12.3932)],
        ["Eur Fermi", (41.8282, 12.4641)],
        ["Flaminio", (41.9142, 12.4751)],
        ["Ostiense", (41.8759, 12.4803)],
        ["Viale Marconi", (41.8425, 12.4719)],
        ["Vittorio Emanuele", (41.8960, 12.5090)],
        ["Monte Mario", (41.9248, 12.4455)],
        ["Piazza Cavour", (41.9051, 12.4665)],
        ["Porta Maggiore", (41.8859, 12.5147)],
        ["Re di Roma", (41.8845, 12.5183)],
        ["Largo Argentina", (41.8956, 12.4764)],
        ["San Paolo", (41.8676, 12.4802)],
        ["Piramide", (41.8754, 12.4815)],
        ["San Lorenzo", (41.8979, 12.5207)],
        ["Ponte Milvio", (41.9327, 12.4750)],
        ["Colli Albani", (41.8694, 12.5339)],
        ["Aurelia", (41.9007, 12.4307)],
        ["Baldo degli Ubaldi", (41.9019, 12.4303)],
        ["San Pietro", (41.9022, 12.4549)],
        ["Porta Pia", (41.9082, 12.4989)]
    ]

    day = datetime.date(2023, 5, 18)
    hour_end = datetime.time(13, 30, 0)


    random.seed(time.time())
    for i in range(sizeUsers):

        stop1 = random.choice(stops)
        stop2 = random.choice(stops)
        create_booking(random.choice(users), stop1[0], stop2[0], day, hour_end, stop1[1][0], stop1[1][1], stop2[1][0], stop2[1][1])
'''


def create_booking_type_end(username, name_start_stop, name_end_stop, date, hour_end,
                            position_start_stop_X, position_start_stop_Y, position_end_stop_X, position_end_stop_Y):
    position_start_stop = WGS84Point((position_start_stop_X, position_start_stop_Y))
    position_end_stop = WGS84Point((position_end_stop_X, position_end_stop_Y))

    # get ID's, and create if not exists
    user_id = dao.create_user(username)
    stop_id_1 = dao.create_stop(name_start_stop, position_start_stop)
    stop_id_2 = dao.create_end_stop(name_end_stop, position_end_stop)
    booking_id = dao.create_booking_type_end(username, name_start_stop, name_end_stop, date, hour_end,
                                             position_start_stop, position_end_stop)
    dao.connect_booking_to_stop(booking_id, user_id, stop_id_1, stop_id_2)

    if dao.search_for_compatibility_type_1(booking_id):
        return
    if dao.search_for_compatibility_type_2(booking_id):
        return
    if dao.search_for_compatibility_type_3(booking_id):
        return


def create_booking_type_start(username, name_start_stop, name_end_stop, date, hour_start,
                              position_start_stop_X, position_start_stop_Y, position_end_stop_X, position_end_stop_Y):
    position_start_stop = WGS84Point((position_start_stop_X, position_start_stop_Y))
    position_end_stop = WGS84Point((position_end_stop_X, position_end_stop_Y))

    # get ID's, and create if not exists
    user_id = dao.create_user(username)
    stop_id_1 = dao.create_stop(name_start_stop, position_start_stop)
    stop_id_2 = dao.create_end_stop(name_end_stop, position_end_stop)
    booking_id = dao.create_booking_type_start(username, name_start_stop, name_end_stop, date, hour_start,
                                               position_start_stop, position_end_stop)
    dao.connect_booking_to_stop(booking_id, user_id, stop_id_1, stop_id_2)

    if dao.search_for_compatibility_type_1(booking_id):
        return
    if dao.search_for_compatibility_type_2(booking_id):
        return
    if dao.search_for_compatibility_type_3(booking_id):
        return


def some_calls():
    # Esempio 1
    create_booking_type_end("Alice", "Termini", "Piazza Venezia", "2023-07-23", "10:15",
                            41.900473, 12.500650, 41.894342, 12.481170)

    # Esempio 2
    create_booking_type_start("Bob", "Colosseo", "San Giovanni", "2023-07-23", "8:30",
                              41.889927, 12.494197, 41.885616, 12.509768)

    # Esempio 3
    create_booking_type_end("Charlie", "Villa Borghese", "Piazza del Popolo", "2023-07-23", "17:45",
                            41.912492, 12.477485, 41.911860, 12.475263)

    '''
    # Esempio 4
    create_booking_type_start("Dave", "Ostia Antica", "Fiumicino Airport", "2023-07-23", "14:00",
                            41.7553, 12.2922, 41.7966, 12.2366)

    # Esempio 5
    create_booking_type_end("Eve", "Castel Sant'Angelo", "Ponte Milvio", "2023-07-23", "12:30",
                            41.9028, 12.4669, 41.9311, 12.4719)

    # Esempio 6
    create_booking_type_start("Frank", "Cinecittà", "Villa Ada", "2023-07-23", "09:45",
                            41.8513, 12.5731, 41.9321, 12.5028)

    # Esempio 7
    create_booking_type_end("Gina", "Villa d'Este", "Tivoli", "2023-07-23", "16:20",
                            41.9624, 12.7949, 41.9679, 12.8006)

    # Esempio 8
    create_booking_type_start("Harry", "Terme di Caracalla", "Aventino", "2023-07-23", "18:00",
                            41.8799, 12.4925, 41.8824, 12.4761)

    # Esempio 9
    create_booking_type_end("Ian", "Villa Adriana", "Villa d'Este", "2023-07-23", "11:15",
                            41.9387, 12.7971, 41.9624, 12.7949)

    # Esempio 10
    create_booking_type_start("Julia", "Catacombe di Priscilla", "Parco degli Acquedotti", "2023-07-23",
                            "14:45",
                            41.9271, 12.4997, 41.8532, 12.5636)
    '''


'''Funzione per inizializzare le code di rabbitMq e ricevere l'handler per la comunicazione, per aggiungere una coda
basta aggiungere un'altra queue declare con il nome della coda che si vuole creare che deve essere univoco, ricordare
che se si hanno più consumer per lo stesso messaggio occorre creare una coda per consumer, sulla quale poi si pubblicheranno
gli stessi messaggi'''


def init_rabbit_mq_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitMq', heartbeat=3600,
                                                                   blocked_connection_timeout=3600))
    channel = connection.channel()
    channel.queue_declare(queue='preparedRoutes1', durable=True)
    return channel


'''Funzione per pubblicare su una coda di rabbit_mq, necessita del channel ricevuto tramite la init, la coda su cui 
si vuole pubblicare e il messaggio da pubblicare, il messaggio deve essere un json array che rappresenta il percorso
in particolare per ogni itinerario si ha un json nell'array fatto come segue:
{"route_expiration": scadenza_percorso, "mail": mail_utente, "it_cost": costo_itinerario_in_euro, 
"it_distance": distanza_itinerario_in_km, "it_departure_time": datetime_partenza_itinerario, 
"it_arrival_time": datetime_arrivo_itinerario, "it_departure_stop": nome_fermata_partenza_itinerario, 
"it_arrival_stop": nome_fermata_arrivo_itinerario}
ad esempio un istanza di tale json array pul essere la seguente:
message=[{"route_expiration": "2023-07-07 00:00:00", "mail": "matteo.conti.977@gmail.com", "it_cost": "5.00",
"it_distance": "12.00", "it_departure_time": "2023-07-08 10:30:00",
"it_arrival_time": "2023-07-08 11:00:00", "it_departure_stop": "Chaddopia",
"it_arrival_stop": "Siummopia"},
{"route_expiration": "2023-07-07 00:00:00", "mail": "lucafalasca08@gmail.com", "it_cost": "3.50",
  "it_distance": "4.00", "it_departure_time": "2023-07-08 10:30:00",
  "it_arrival_time": "2023-07-08 11:00:00", "it_departure_stop": "Sorbona",
  "it_arrival_stop": "Subaugusta (MA)"}] 
notare che il parametro messagge_json va passato come json.dumps(message)
'''


def publish_message_on_queue(message_json, queue, channel):
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message_json.encode('utf-8'),
                          properties=pika.BasicProperties(delivery_mode=2))
    print("Sent message on queue: " + queue)


def test_rabbitMq(channel):
    message = [
        {"route_expiration": "2023-07-07 00:00:00", "mail": "matteo.conti.977@gmail.com", "it_cost": "5.00",
         "it_distance": "12.00", "it_departure_time": "2023-07-08 10:30:00",
         "it_arrival_time": "2023-07-08 11:00:00", "it_departure_stop": "Chaddopia",
         "it_arrival_stop": "Siummopia"}
    ]
    publish_message_on_queue(json.dumps(message), 'preparedRoutes1', channel)


def insert_booking(user, starting_point, start_lat, start_lng, ending_point, end_lat, end_lng, date, start_or_finish,
                   time):
    create_booking_type_start(user, starting_point, ending_point, date, time, start_lat, start_lng, end_lat, end_lng)
    return True


def json_to_route_info(json_input):
    order_list = []
    it_list = []

    route_expiration = datetime.datetime.strptime(json_input['steps'][0]['date'], '%Y-%m-%d')

    for step in json_input['steps']:
        order_list.append([int(step['id']), step['location'][1], step['location'][0]])

    for username, route in json_input['user_routes'].items():
        start_stop = json_input['steps'][int(route[0])]
        end_stop = json_input['steps'][int(route[-1])]
        it_list.append(
            [0, 0, start_stop['date'] + " " + start_stop['time'], end_stop['date'] + " " + end_stop['time'], username,
             1,
             start_stop['location'][1], start_stop['location'][0],
             end_stop['location'][1], end_stop['location'][0]])

    return str(route_expiration), order_list, it_list,


def propose_route_callback(ch, method, properties, body):
    json_return = json.loads(body.decode('utf-8'))
    print("Received prepared routes message: \n" + json.dumps(json_return))

    route_expiration, order_list, it_list = json_to_route_info(json_return)

    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        proxy.insert_route_info(route_expiration, order_list, it_list)


def serverRPCThread():
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Server RPC is ON on port 8000")
    server.register_function(insert_booking, "insert_booking")
    server.serve_forever()


def rabbitMQThread():
    # create queues for rabbitMq the channel has to be passed as parameter to publish function
    queue_channel = init_rabbit_mq_queues()  # queue_connection va ammmazzata quando non serve piu
    # test_rabbitMq(queue_channel)

    # Coda da consumer per ricevere i messaggi di makeRouteService
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitMq', heartbeat=3600,
                                                                   blocked_connection_timeout=3600))
    channel = connection.channel()
    # Create a queue, if already exist nothing happens
    channel.queue_declare(queue=PROPOSE_ROUTE_QUEUE, durable=True)
    channel.basic_consume(queue=PROPOSE_ROUTE_QUEUE,
                          auto_ack=True,
                          on_message_callback=propose_route_callback)

    print("I'm waiting for messages on queue [" + PROPOSE_ROUTE_QUEUE + "]...")
    channel.start_consuming()


if __name__ == "__main__":
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    some_calls()
    dao.close()

    prova = {
        "steps": [
            {
                "id": "2",
                "date": "2023-07-23",
                "time": "17:48:00",
                "location": [
                    12.375458,
                    42.028740
                ]
            },
            {
                "id": "0",
                "date": "2023-07-23",
                "time": "18:00:00",
                "location": [
                    12.374834,
                    42.051147
                ]
            },
            {
                "id": "1",
                "date": "2023-07-23",
                "time": "18:06:00",
                "location": [
                    12.448636,
                    42.029957
                ]
            },
            {
                "id": "3",
                "date": "2023-07-23",
                "time": "18:21:00",
                "location": [
                    12.469408,
                    42.032089
                ]
            }
        ],
        "travel_time": "0:33:00",
        "n_tardy": 2,
        "mean_unacceptable_deviance": "1:59:00",
        "users_travel_time": {
            "persona1": "0:06:00",
            "persona2": "0:06:00",
            "persona3": "0:33:00"
        },
        "user_routes": {
            "prova@gmail.com": [
                "0",
                "1"
            ],
            "prova@gmail.com": [
                "0",
                "1"
            ],
            "prova@gmail.com"

            : [
                "2",
                "3"
            ]
        }
    }
    route_expiration, order_list, it_list = json_to_route_info(prova)

    print("ROUTE EXPIRATION:\n" + str(route_expiration))
    print("\nORDER_LIST\n" + str(order_list))
    print("\nIT_LIST\n" + str(it_list))

    # with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
    # res = proxy.insert_route_info(route_expiration, order_list, it_list)
    # print("annata bene? " + str(res))

    rpcThread = threading.Thread(target=serverRPCThread)
    queueThread = threading.Thread(target=rabbitMQThread)
    rpcThread.start()
    queueThread.start()

    rpcThread.join()
    queueThread.join()
