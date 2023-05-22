import xmlrpc.server
import random
import time

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
    remove_duplicates(route)
    print(route)
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

def remove_duplicates(route):
    new_list = []
    for item in route:
        if item not in new_list:
            new_list.append(item)
    route[:] = new_list

if __name__ == "__main__":
    route = [0, 1, 3]
    dist_matrix = generate_dist_matrix(5, 10)
    pred_hash = {"0": [1, 3]}

    print(two_opt_multistart(route, dist_matrix, pred_hash, 1))

    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    server.register_function(two_opt_multistart, "two_opt_multistart")
    server.serve_forever()