import random
import time
import xmlrpc.server
from collections import deque
import json
import queue
import datetime
import threading

import pika

import compact as alg2


def two_opt(route, dist_matrix, prec_hash, node_limit):
    alternative_route = []
    n = max(route) + 1
    improvement = True
    best_route = route
    route_string = [str(i) for i in route]
    final_route, best_distance, best_n_tardy, best_tardy_mean, _, _, _ = alg2.compact(route_string, dist_matrix,
                                                                                      node_limit)
    while improvement:
        improvement = False
        for i in range(0, n):
            for j in range(i, n):
                if i == j:
                    continue
                if i not in route or j not in route:
                    continue
                new_route = route[:]
                new_route[route.index(i)] = route[route.index(j)]
                new_route[route.index(j)] = route[route.index(i)]

                if not check_prec(new_route, prec_hash):
                    continue

                new_route_string = [str(i) for i in new_route]
                new_final_route, new_distance, new_n_tardy, new_tardy_mean, _, _, _ = alg2.compact(new_route_string,
                                                                                                   dist_matrix,
                                                                                                   node_limit)
                if is_better([new_n_tardy, new_tardy_mean, new_distance],
                             [best_n_tardy, best_tardy_mean, best_distance]):
                    best_n_tardy = new_n_tardy
                    best_tardy_mean = new_tardy_mean
                    best_route = new_route
                    best_distance = new_distance
                    final_route = new_final_route
                    improvement = True
                else:
                    alternative_route.append(new_route)
        route = best_route
    return final_route, best_distance, best_n_tardy, best_tardy_mean, alternative_route


def route_distance(route, dist_matrix):
    distance = 0
    for i in range(len(route) - 1):
        distance += dist_matrix[route[i]][route[i + 1]]
    return distance


def check_prec(route, prec_hash):
    for i in prec_hash:
        for j in prec_hash[str(i)]:
            if (route.index(int(i)) > route.index(int(j))):
                return False
    return True


def is_better(new, old):
    if len(new) == 0:
        return True
    if new[0] < old[0]:
        return True
    elif new[0] > old[0]:
        return False
    else:
        return is_better(new[1:], old[1:])


def two_opt_multistart(route, dist_matrix, prec_hash, node_limit, multistart_number):
    result = two_opt(route, dist_matrix, prec_hash, node_limit)
    if result == None:
        return None

    resultMin = result
    best_distance = result[2]
    best_n_tardy = result[3]
    best_tardy_mean = result[4]
    alternativeRoute = result[4]
    for altRoute in alternativeRoute[:multistart_number - 1]:
        result = two_opt(altRoute, dist_matrix, prec_hash, node_limit)
        if (result[1] < min):
            min = result[1]
            resultMin = result
    return result[:-1]


# only for throuble shooting
def generate_dist_matrix(size, max_val):
    random.seed(time.time())
    dist_matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(0)
            else:
                val = random.randint(1, max_val)
                row.append(val)
        dist_matrix.append(row)
    return dist_matrix


def remove_duplicates(nodes):
    nodes = list(set(nodes))


def topological_sort(graph):
    # Inizializza il conteggio delle dipendenze per ogni nodo del grafo
    in_degree = {node: 0 for node in graph}
    # Calcola il conteggio delle dipendenze per ogni nodo del grafo
    for node in graph:
        for neighbor in graph[node]:
            in_degree[str(neighbor)] += 1

    # Inizializza la coda di lavoro con i nodi senza dipendenze
    queue = deque([node for node in in_degree if in_degree[node] == 0])

    # Inizializza l'ordinamento topologico
    topological_order = []

    # Ripeti finché la coda non è vuota
    while queue:
        # print(queue)
        # Prende un nodo dalla coda
        node = queue.popleft()

        # Aggiunge il nodo all'ordinamento topologico
        topological_order.append(int(node))

        # Aggiorna il conteggio delle dipendenze per ogni vicino del nodo
        for neighbor in graph[node]:
            in_degree[str(neighbor)] -= 1

            # Se il vicino non ha dipendenze, lo aggiunge alla coda
            if in_degree[str(neighbor)] == 0:
                queue.append(str(neighbor))

    # Restituisce l'ordinamento topologico, se esiste
    if len(topological_order) == len(graph):
        return topological_order
    else:
        return None


# Algoritmo per il calcolo della rotta migliore
# Input: matrice delle distanze, dizionario delle precedenze, dizionario dei limiti di tempo, dizionario delle rotte degli utenti
# Output: tupla contenente la rotta migliore e il dizionario dei tempi di percorrenza degli utenti
def calculate_route(dist_matrix, prec_hash, node_limit, user_routes):
    node_list = list(map(int, prec_hash.keys()))
    remove_duplicates(node_list)
    route = topological_sort(prec_hash)
    result = two_opt_multistart(route, dist_matrix, prec_hash, node_limit, 1)
    if result == None:
        return None
    else:
        final_ruote = result[0]
        user_travel_time = {}
        ruote_dict = {tup[0]: tup[1] for tup in final_ruote}
        for route in user_routes:
            user_travel_time[route["it_id"]] = str(datetime.timedelta(
                minutes=round((float(ruote_dict[route["nodes"][1]]) - float(ruote_dict[route["nodes"][0]])), 0)))
        return result, user_travel_time


def prepared_routes_callback(ch, method, properties, body):
    json_return = json.loads(body.decode('utf-8'))
    print("Received prepared routes message: \n" + json.dumps(json_return, indent=2))
    # INSERIRE IL CODICE PER GESTIRE IL MESSAGGIO RICEVUTO
    message = json.loads(body.decode('utf-8'))
    node_limit = message["node_limit"]
    prec_hash = message["prec_hash"]
    dist_matrix = message["dist_matrix"]
    user_routes = message["user_routes"]
    date_string = user_routes[0]["date"]
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    result = calculate_route(dist_matrix, prec_hash, node_limit, user_routes)
    print("Result : " + str(result))
    result_json = {}
    route = result[0][0]
    steps = []
    for step in route:
        step_json = {}
        step_json["id"] = step[0]
        time = round(float(step[1]), 0)
        if time > 0 and time < 1440:
            step_json["date"] = str(date)[0:10]
            step_json["time"] = str(datetime.timedelta(minutes=(time)))
        elif time < 0:
            step_json["date"] = str(date + datetime.timedelta(days=-1))[0:10]
            step_json["time"] = str(datetime.timedelta(minutes=1440 + time))
        elif time > 1440:
            step_json["date"] = str(date + datetime.timedelta(days=1))[0:10]
            step_json["time"] = str(datetime.timedelta(minutes=time - 1440))
        step_json["location"] = message["points_location"][str(step[0])][::-1]
        steps.append(step_json)
    result_json["steps"] = steps
    result_json["travel_time"] = str(datetime.timedelta(minutes=round(float(result[0][1]), 0)))
    result_json["n_tardy"] = result[0][2]
    result_json["mean_unacceptable_deviance"] = str(datetime.timedelta(minutes=round(result[0][3])))
    result_json["users_travel_time"] = result[1]
    result_json["user_routes"] = user_routes
    queue.publish_message_on_queue(json.dumps(result_json), queue.PROPOSE_ROUTE_QUEUE, queue_channel_pub)


def rabbitMQThreadConsumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitMq', heartbeat=3600,
                                                                   blocked_connection_timeout=3600))
    channel = connection.channel()
    # Create a queue, if already exist nothing happens
    channel.queue_declare(queue=queue.MAKE_ROUTE_STOP_DATA_QUEUE_1, durable=True)
    channel.basic_consume(queue=queue.MAKE_ROUTE_STOP_DATA_QUEUE_1,
                          auto_ack=True,
                          on_message_callback=prepared_routes_callback)

    print("I'm waiting for messages on queue [" + queue.MAKE_ROUTE_STOP_DATA_QUEUE_1 + "]...")
    channel.start_consuming()


def serverRPCThread():
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Server RPC is ON on port 8000")

    server.register_function(calculate_route, "calculate_route")
    server.serve_forever()


if __name__ == "__main__":
    queue_channel_pub = queue.init_rabbit_mq_queues()  # queue_connection va ammmazzata quando non serve piu

    queueConsumerThread = threading.Thread(target=rabbitMQThreadConsumer)
    serverRPCThread = threading.Thread(target=serverRPCThread)

    queueConsumerThread.start()
    serverRPCThread.start()

    queueConsumerThread.join()
    serverRPCThread.join()
