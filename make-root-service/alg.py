import xmlrpc.server

def two_opt(route, dist_matrix, pred_hash):
    alternative_route = []
    n = len(route)
    improvement = True
    best_route = route
    best_distance = route_distance(route, dist_matrix)
    while improvement:
        improvement = False
        for i in range(0, n - 1):
            for j in range(i, n - 1):
                if i == j:
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
        if(route.index(int(i)) > route.index(pred_hash[str(i)])):
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

if __name__ == "__main__":
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    server.register_function(two_opt_multistart, "two_opt_multistart")
    server.serve_forever()