import datetime
import json
import threading
import xmlrpc.client
import xmlrpc.server

import pika
from neo4j._spatial import WGS84Point

from Neo4jDAO_BS import *

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


def create_booking_type_end(it_id, username, name_start_stop, name_end_stop, date, hour_end,
                            position_start_stop_X, position_start_stop_Y, position_end_stop_X, position_end_stop_Y):
    position_start_stop = WGS84Point((position_start_stop_X, position_start_stop_Y))
    position_end_stop = WGS84Point((position_end_stop_X, position_end_stop_Y))

    # get ID's, and create if not exists
    user_id = dao.create_user(username)
    stop_id_1 = dao.create_stop(name_start_stop, position_start_stop)
    stop_id_2 = dao.create_end_stop(name_end_stop, position_end_stop)
    booking_id = dao.create_booking_type_end(it_id, username, name_start_stop, name_end_stop, date, hour_end,
                                             position_start_stop, position_end_stop)
    dao.connect_booking_to_stop(booking_id, user_id, stop_id_1, stop_id_2)
    print("BOOKING_ID_PERA" + str(booking_id))

    if dao.search_for_compatibility_type_1(booking_id):
        dao.get_compatible_time_bookings(booking_id)
        return booking_id
    if dao.search_for_compatibility_type_2(booking_id):
        dao.get_compatible_time_bookings(booking_id)
        return booking_id
    if dao.search_for_compatibility_type_3(booking_id):
        dao.get_compatible_time_bookings(booking_id)
        return booking_id


def create_booking_type_start(it_id, username, name_start_stop, name_end_stop, date, hour_start,
                              position_start_stop_X, position_start_stop_Y, position_end_stop_X, position_end_stop_Y):

    position_start_stop = WGS84Point((position_start_stop_X, position_start_stop_Y))
    position_end_stop = WGS84Point((position_end_stop_X, position_end_stop_Y))

    # get ID's, and create if not exists
    user_id = dao.create_user(username)
    stop_id_1 = dao.create_stop(name_start_stop, position_start_stop)
    stop_id_2 = dao.create_end_stop(name_end_stop, position_end_stop)
    booking_id = dao.create_booking_type_start(it_id, username, name_start_stop, name_end_stop, date, hour_start,
                                               position_start_stop, position_end_stop)
    dao.connect_booking_to_stop(booking_id, user_id, stop_id_1, stop_id_2)
    print("BOOKING_ID_PERA" + str(booking_id))


    if dao.search_for_compatibility_type_1(booking_id):
        dao.get_compatible_time_bookings(booking_id)
        return booking_id
    if dao.search_for_compatibility_type_2(booking_id):
        dao.get_compatible_time_bookings()
        return booking_id
    if dao.search_for_compatibility_type_3(booking_id):
        dao.get_compatible_time_bookings()
        return booking_id





'''Funzione per inizializzare le code di rabbitMq e ricevere l'handler per la comunicazione, per aggiungere una coda
basta aggiungere un'altra queue declare con il nome della coda che si vuole creare che deve essere univoco, ricordare
che se si hanno più consumer per lo stesso messaggio occorre creare una coda per consumer, sulla quale poi si pubblicheranno
gli stessi messaggi'''


def init_rabbit_mq_notify_queues():
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
    id_book = None
    if start_or_finish == "start":
        print("Ciao dovrei stare qui dentro")
        with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
            it_id = json.loads(proxy.insert_it_req(date + " " + time, 0.0, user, start_lat, start_lng, end_lat, end_lng, 1))
        id_book = create_booking_type_start(it_id, user, starting_point, ending_point, date, time, start_lat, start_lng, end_lat,
                                  end_lng)
    else:
        with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
            it_id = json.loads(proxy.insert_it_req(date + " " + time, 0.0, user, start_lat, start_lng, end_lat, end_lng, 0))
        id_book = create_booking_type_end(it_id, user, starting_point, ending_point, date, time, start_lat, start_lng, end_lat, end_lng)
    with xmlrpc.client.ServerProxy("http://node-selector-service:8000/") as proxy:
        print("id_book: " + str(id_book))
        if(id_book != None):
            print("sto per fare la richiesta rpc")
            proxy.send_nodes_for_computation(id_book)
            print("ho fatto la richiesta rpc")
    print("Funziono?")
    return True


def json_to_route_info(json_input):
    print(json_input)
    order_list = []
    it_list = []
    nodes = [0 for q in json_input['steps']]
    print(nodes)

    route_expiration = datetime.datetime.now() + datetime.timedelta(hours = 12)
    print("route_expiration default: " + str(route_expiration))


    
    for step in json_input['steps']:
        order_list.append([int(step['id']), step['location'][1], step['location'][0]])
        nodes[int(step['id'])] = [step['location'][0], step['location'][1]]

    print(nodes)
    with xmlrpc.client.ServerProxy("http://ors-dao:8000/") as proxy:
        matrix_distance = proxy.get_matrix_distance(nodes)

    total_distance = 0
    for i in range(len(order_list) - 1):
        total_distance += matrix_distance[order_list[i][0]][order_list[i + 1][0]]

    total_metres = 0
    for tour in json_input['user_routes']:
        metres = matrix_distance[int(tour["nodes"][0])][int(tour["nodes"][1])]
        total_metres += metres

    lt_per_km = 0.08
    fuel_price = 1.85
    price_per_km = lt_per_km * fuel_price
    # supplemento del costo dovuto al fatto che il 35% delle persone potrebbe rifiutare il percorso
    supplement_due_refuse = 1.35
    # supplemento del costo dovuto al fatto che il 50% del costo è profitto
    supplement_due_profit = 1.5

    fixed_price = 0.50

    total_price = (total_distance / 1000 * price_per_km * supplement_due_refuse + fixed_price) * supplement_due_profit
    print("Total distance: " + str(total_distance))
    print("Total metres: " + str(total_metres))
    print("Total price: " + str(total_price))
    

    print("nodes: " + str(nodes))
    print(json_input['user_routes'])
    min_time = datetime.datetime.strptime(json_input['steps'][0]['date'] + " " + json_input['steps'][0]['time'], '%Y-%m-%d %H:%M:%S')
    for tour in json_input['user_routes']:
        start_stop = get_step_from_node_number(json_input['steps'], tour["nodes"][0])
        end_stop = get_step_from_node_number(json_input['steps'], tour["nodes"][1])

        print("start_stop: " + str(start_stop))
        print("end_stop: " + str(end_stop))
        metres = matrix_distance[int(tour["nodes"][0])][int(tour["nodes"][1])]
        it_id = tour["it_id"]
        weight = metres / total_metres
        price = total_price * weight
        if(datetime.datetime.strptime(start_stop['date'] + " " + start_stop['time'], '%Y-%m-%d %H:%M:%S') < min_time):
            min_time = datetime.datetime.strptime(start_stop['date'] + " " + start_stop['time'], '%Y-%m-%d %H:%M:%S')
        print()
        it_list.append([
            round(price, 2),                                                #prezzo
            round(metres / 1000, 3),                                        #distanza
            start_stop['date'] + " " + start_stop['time'],                  #data e ora di partenza
            end_stop['date'] + " " + end_stop['time'], tour["user"],        #data e ora di arrivo
            it_id,                                                          #id dellítinerario richiesto
            start_stop['location'][1], start_stop['location'][0],           #lat e lng di partenza
            end_stop['location'][1], end_stop['location'][0]])              #lat e lng di arrivo

    delta = (min_time - datetime.datetime.now()) / 2
    print("delta: " + str(delta))
    route_expiration = min(route_expiration, min_time - delta)
    print("route_expiration: " + str(route_expiration))
    return str(route_expiration), order_list, it_list,

def get_step_from_node_number(steps, node_number):
    for i in range(len(steps)):
        if steps[i]['id'] == node_number:
            return steps[i]
    return -1


def propose_route_callback(ch, method, properties, body):
    json_return = json.loads(body.decode('utf-8'))
    print("Received prepared routes message: \n" + json.dumps(json_return))

    route_expiration, order_list, it_list = json_to_route_info(json_return)
    print("ROUTE EXPIRATION:\n" + str(route_expiration))
    print("\nORDER_LIST\n" + str(order_list))
    print("\nIT_LIST\n" + str(it_list))
    res = None
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        res = proxy.insert_route_info(route_expiration, order_list, it_list)
    if res['status'] == "ok":
        print("Route info inserted correctly")
        message_list= []
        for elem in it_list:
            with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
                start_stop = json.loads(proxy.get_stop_name_from_coords(elem[6], elem[7]))
            with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
                end_stop = json.loads(proxy.get_stop_name_from_coords(elem[8], elem[9]))
            message = {'route_expiration': route_expiration, 'mail': elem[4], 'it_cost': elem[0],
                       'it_distance': elem[1], 'it_departure_time': elem[2], 'it_arrival_time': elem[3],
                       'it_departure_stop': start_stop, 'it_arrival_stop': end_stop}
            message_list.append(message)
        # create queues for rabbitMq the channel has to be passed as parameter to publish function
        notify_channel = init_rabbit_mq_notify_queues()  # queue_connection va ammmazzata quando non serve piu
        # test_rabbitMq(queue_channel)
        publish_message_on_queue(json.dumps(message_list), 'preparedRoutes1', notify_channel)
        notify_channel.close()


def serverRPCThread():
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Server RPC is ON on port 8000")
    server.register_function(insert_booking, "insert_booking")
    server.serve_forever()


def rabbitMQThread():

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
    #some_calls()
    #print(dao.get_start_end_bookings_with_limit(8,10))
    dao.close()


    print("*********")



    '''prova = {
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
            "prova1@gmail.com": [
                "0",
                "1"
            ],
            "prova2@gmail.com": [
                "0",
                "1"
            ],
            "prova3@gmail.com": [
                "2",
                "3"
            ]
        }
    }

    route_expiration, order_list, it_list = json_to_route_info(prova)

    print("ROUTE EXPIRATION:\n" + str(route_expiration))
    print("\nORDER_LIST\n" + str(order_list))
    print("\nIT_LIST\n" + str(it_list))'''

    # with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
    # res = proxy.insert_route_info(route_expiration, order_list, it_list)
    # print("annata bene? " + str(res))

    rpcThread = threading.Thread(target=serverRPCThread)
    queueThread = threading.Thread(target=rabbitMQThread)
    rpcThread.start()
    queueThread.start()

    rpcThread.join()
    queueThread.join()

