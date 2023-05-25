import xmlrpc.server
import random
import time
from collections import deque

def two_opt(route, dist_matrix, pred_hash):
    alternative_route = []
    n = max(route) + 1
    improvement = True
    best_route = route
    best_distance = route_distance(route, dist_matrix)
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

                if not check_pred(new_route, pred_hash):
                    continue
                new_distance = route_distance(new_route, dist_matrix)
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_route = new_route
                    improvement = True
                else:
                    alternative_route.append(new_route)
        route = best_route
    return best_route, best_distance, alternative_route


def route_distance(route, dist_matrix):
    distance = 0
    for i in range(len(route) - 1):
        distance += dist_matrix[route[i]][route[i+1]]
    return distance

def check_pred(route, pred_hash):
    for i in pred_hash:
        for j in pred_hash[str(i)]:
            if(route.index(int(i)) > route.index(j)):
                return False
    return True

def two_opt_multistart(route, dist_matrix, pred_hash, multistart_number):
    result = two_opt(route, dist_matrix, pred_hash)
    resultMin = result
    min = result[1]
    alternativeRoute = result[2]
    for altRoute in alternativeRoute[:multistart_number-1]:
        result = two_opt(altRoute, dist_matrix, pred_hash)
        if(result[1] < min):
            min = result[1]
            resultMin = result
    return resultMin[:2]

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
    print(in_degree)
    # Calcola il conteggio delle dipendenze per ogni nodo del grafo
    for node in graph:
        for neighbor in graph[node]:
            print(graph[node])
            in_degree[str(neighbor)] += 1
    print(in_degree)

    # Inizializza la coda di lavoro con i nodi senza dipendenze
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    
    # Inizializza l'ordinamento topologico
    topological_order = []

    # Ripeti finché la coda non è vuota
    while queue:
        print(queue)
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

def calculate_route(dist_matrix, pred_hash):
    node_list = list(map(int, pred_hash.keys()))
    remove_duplicates(node_list)
    route = topological_sort(pred_hash)
    print(route)
    if(route == None):
        return None
    else:
        return two_opt_multistart(route, dist_matrix, pred_hash, 10)

if __name__ == "__main__":
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    server.register_function(calculate_route, "calculate_route")
    server.serve_forever()