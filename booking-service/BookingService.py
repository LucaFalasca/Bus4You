import json

import pika
import xmlrpc.server

from neo4j import GraphDatabase, basic_auth
from neo4j._spatial import WGS84Point
from Neo4jDAO import *
from NodeToAlg import *
from Node import *
from utils import *

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
    create_booking_type_end("Alice", "Termini", "Piazza Venezia", datetime.date(2023, 7, 23), datetime.time(10, 15),
                            41.9014, 12.5005, 41.8954, 12.4823)

    # Esempio 2
    create_booking_type_start("Bob", "Colosseo", "San Giovanni", datetime.date(2023, 7, 23), datetime.time(8, 30),
                            41.8902, 12.4924, 41.8743, 12.5110)

    # Esempio 3
    create_booking_type_end("Charlie", "Villa Borghese", "Piazza del Popolo", datetime.date(2023, 7, 23), datetime.time(17, 45),
                            41.9142, 12.4921, 41.9098, 12.4767)

    # Esempio 4
    create_booking_type_start("Dave", "Ostia Antica", "Fiumicino Airport", datetime.date(2023, 7, 23), datetime.time(14, 0),
                            41.7553, 12.2922, 41.7966, 12.2366)

    # Esempio 5
    create_booking_type_end("Eve", "Castel Sant'Angelo", "Ponte Milvio", datetime.date(2023, 7, 23), datetime.time(12, 30),
                            41.9028, 12.4669, 41.9311, 12.4719)

    # Esempio 6
    create_booking_type_start("Frank", "Cinecittà", "Villa Ada", datetime.date(2023, 7, 23), datetime.time(9, 45),
                            41.8513, 12.5731, 41.9321, 12.5028)

    # Esempio 7
    create_booking_type_end("Gina", "Villa d'Este", "Tivoli", datetime.date(2023, 7, 23), datetime.time(16, 20),
                            41.9624, 12.7949, 41.9679, 12.8006)

    # Esempio 8
    create_booking_type_start("Harry", "Terme di Caracalla", "Aventino", datetime.date(2023, 7, 23), datetime.time(18, 0),
                            41.8799, 12.4925, 41.8824, 12.4761)

    # Esempio 9
    create_booking_type_end("Ian", "Villa Adriana", "Villa d'Este", datetime.date(2023, 7, 23), datetime.time(11, 15),
                            41.9387, 12.7971, 41.9624, 12.7949)

    # Esempio 10
    create_booking_type_start("Julia", "Catacombe di Priscilla", "Parco degli Acquedotti", datetime.date(2023, 7, 23),
                            datetime.time(14, 45),
                            41.9271, 12.4997, 41.8532, 12.5636)


'''Funzione per inizializzare le code di rabbitMq e ricevere l'handler per la comunicazione, per aggiungere una coda
basta aggiungere un'altra queue declare con il nome della coda che si vuole creare che deve essere univoco, ricordare
che se si hanno più consumer per lo stesso messaggio occorre creare una coda per consumer, sulla quale poi si pubblicheranno
gli stessi messaggi'''
def init_rabbit_mq_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitMq'))
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

def insert_booking(user, starting_point, start_lat, start_lng, ending_point, end_lat, end_lng, date, start_or_finish, time):
    s = "user: " + user + " starting_point: " + starting_point + " start_lat: " + str(start_lat) + " start_lng: " + str(start_lng) + " ending_point: " + ending_point + " end_lat: " + str(end_lat) + " end_lng: " + str(end_lng) + " date: " + str(date) + " start_or_finish: " + start_or_finish + " time: " + str(time)
    print(s)
    return True

def propose_route_callback(ch, method, properties, body):
    print("Received prepared routes message: " + body.decode('utf-8'))


if __name__ == "__main__":
    
    # create queues for rabbitMq the channel has to be passed as parameter to publish function
    queue_channel= init_rabbit_mq_queues()  # queue_connection va ammmazzata quando non serve piu
    #test_rabbitMq(queue_channel)
    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    some_calls()

    '''
    

    create_booking_type_start("Stefan", "Termini", "Piazza Venezia", datetime.date(2023, 5, 18), datetime.time(13, 30, 0),
                            41.9014, 12.5005, 41.8954, 12.4823)

    create_booking_type_end("Luca", "Colosseo", "Monte Mario", datetime.date(2023, 5, 18), datetime.time(14, 30, 0),
                            41.8902, 12.4923, 41.9248, 12.4455)
    

    toAlg = NodeToAlg(dao)
    #print_node_list(toAlg.take_nodes_from_bd(18))
    #print(str(dao.get_distances(16, 17)))

    dao.close()

    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")
    server.register_function(insert_booking, "insert_booking")
    server.serve_forever()
    # session.close()
    '''

    # Coda da consumer per ricevere i messaggi di makeRouteService
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitMq'))
    channel = connection.channel()
    # Create a queue, if already exist nothing happens
    channel.queue_declare(queue = PROPOSE_ROUTE_QUEUE, durable = True)
    channel.basic_consume(queue = PROPOSE_ROUTE_QUEUE,
                          auto_ack = True,
                          on_message_callback = propose_route_callback)

    print("Sto ascoltando")
    channel.start_consuming()
