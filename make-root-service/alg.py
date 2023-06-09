import xmlrpc.server
import random
import time
from collections import deque
from enum import Enum
import datetime
import alg2

class NodeState(Enum):
        RIGHT_FIXED = 1
        LEFT_FIXED = 2
        NOT_FIXED = 3
        FIXED = 4

def two_opt(route, dist_matrix, prec_hash, travel_time_matrix, node_limit):
    alternative_route = []
    n = max(route) + 1
    improvement = True
    best_route = route
    route_string = [str(i) for i in route]
    final_route , best_distance, best_n_tardy, best_tardy_mean, _, _, _ = alg2.compact(route_string, dist_matrix, node_limit)
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
                final_route , new_distance, new_n_tardy, new_tardy_mean, _, _, _ = alg2.compact(new_route_string, dist_matrix, node_limit)
                #print("CurrentRoute: " + str(best_route) + " - newRoute: " + str(new_route))
                #print("CurrentDistance: " + str(best_distance) + " - newDistance: " + str(new_distance))
                #print("CurrentTard: " + str(best_n_tardy) + " - newTard: " + str(new_n_tardy))
                #print("CurrentTardMean: " + str(best_tardy_mean) + " - newTardMean: " + str(new_tardy_mean))
                if new_n_tardy < best_n_tardy or new_n_tardy == best_n_tardy and new_tardy_mean < best_tardy_mean:
                    best_n_tardy = new_n_tardy
                    best_tardy_mean = new_tardy_mean
                    best_route = new_route
                    best_distance = new_distance
                    improvement = True
                    #print("Improvement")
                else:
                    alternative_route.append(new_route)
        route = best_route
    return final_route, best_distance, best_n_tardy, best_tardy_mean, alternative_route

def tardy_mean(route, dist_matrix, pred_hash, travel_time_matrix):
    sum = 0
    c = 0
    for k in pred_hash:
        for v in pred_hash[k]:
            subroute = route[route.index(int(k)):route.index(v) + 1]
            sum += calculate_tardiness(subroute, dist_matrix, travel_time_matrix)
            c += 1
    return sum / c

def number_of_tardy_routes(route, dist_matrix, pred_hash, travel_time_matrix):
    count = 0
    for k in pred_hash:
        for v in pred_hash[k]:
            subroute = route[route.index(int(k)):route.index(v) + 1]
            if calculate_tardiness(subroute, dist_matrix, travel_time_matrix) > 0:
                count += 1
    return count

def calculate_tardiness(route, dist_matrix, travel_time_matrix):
    return max(0, route_distance(route, dist_matrix) - travel_time_matrix[route[0]][route[-1]])


def route_distance(route, dist_matrix):
    distance = 0
    for i in range(len(route) - 1):
        distance += dist_matrix[route[i]][route[i+1]]
    return distance

def check_prec(route, prec_hash):
    for i in prec_hash:
        for j in prec_hash[str(i)]:
            if(route.index(int(i)) > route.index(int(j))):
                return False
    return True

def check_travel_time(route, dist_matrix, travel_time_matrix):
    for i in range(len(dist_matrix)):
        for j in range(len(dist_matrix)):
            if travel_time_matrix[i][j] != 0:
                start = route.index(i)
                end = route.index(j)
                if route_distance(route[start : end], dist_matrix) > travel_time_matrix[i][j]:
                    return False
    return True


def two_opt_multistart(route, dist_matrix, prec_hash, travel_time_matrix, node_limit, multistart_number):
    result = two_opt(route, dist_matrix, prec_hash, travel_time_matrix, node_limit)
    if result == None:
        return None
    '''
    resultMin = result
    min = result[2]
    alternativeRoute = result[3]
    for altRoute in alternativeRoute[:multistart_number-1]:
        result = two_opt(altRoute, dist_matrix, prec_hash, travel_time_matrix, node_limit)
        if(result[1] < min):
            min = result[1]
            resultMin = result
    '''
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
    #print(in_degree)
    # Calcola il conteggio delle dipendenze per ogni nodo del grafo
    for node in graph:
        for neighbor in graph[node]:
            #print(graph[node])
            in_degree[str(neighbor)] += 1
    #print(in_degree)

    # Inizializza la coda di lavoro con i nodi senza dipendenze
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    
    # Inizializza l'ordinamento topologico
    topological_order = []

    # Ripeti finché la coda non è vuota
    while queue:
        #print(queue)
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

def calculate_route(dist_matrix, prec_hash, travel_time_matrix, node_limit, user_ruotes):
    node_list = list(map(int, prec_hash.keys()))
    remove_duplicates(node_list)
    route = topological_sort(prec_hash)
    result = two_opt_multistart(route, dist_matrix, prec_hash, travel_time_matrix, node_limit, 1)
    if result == None:
        return None
    else:
        final_ruote = result[0]
        user_travel_time = {}
        ruote_dict = {tup[0]:tup[1] for tup in final_ruote}
        for user in user_routes:
            user_travel_time[user] = float(ruote_dict[user_routes[user][1]]) - float(ruote_dict[user_routes[user][0]])
        return result, user_travel_time

if __name__ == "__main__":
    node_limit = {'1': (None, datetime.time(13, 55)),
			'3': (datetime.time(14, 10), datetime.time(14, 40)),
			'5': (datetime.time(14, 45), None)}
    prec_hash = {'0': ['1'], '1': [], '2': ['3'], '3': [], '4': ['5'], '5': []}
    dist_matrix =  [[0, 20, 10, 30, 20, 30],
					[20, 0, 10, 20, 10, 20],
					[10, 10, 0, 20, 10, 20],
					[30, 20, 20, 0, 10, 10],
					[20, 10, 10, 10, 0, 10],
					[30, 20, 20, 10, 10, 0]]
    user_routes = {"Giovanni": ('0', '1'),
                    "Marco": ('2', '3'),
                    "Luca": ('4', '5')}

    node_limit_min = {k : (alg2.convert_time_to_minutes(v[0]), alg2.convert_time_to_minutes(v[1])) for k, v in node_limit.items()}
    
    result = calculate_route(dist_matrix, prec_hash, None, node_limit_min, user_routes)
    if result == None:
        print("No route found")
    else:
        print(result)
    '''
    else:
        route = result[0]
        print(route)
        print(result)
        for k in prec_hash:
            for v in prec_hash[k]:
                subroute = route[route.index(int(k)):route.index(int(v)) + 1]
                print(subroute)
                print("distance: " + str(route_distance(subroute, dist_matrix)))
    '''
    
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    server.register_function(calculate_route, "calculate_route")
    server.serve_forever()
    


   

    