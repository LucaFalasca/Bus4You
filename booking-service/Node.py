class Node:

    def __init__(self, starting_point, ending_point, data, arrival_time, booking, travel_time="30:00"):
        self.starting_point = starting_point
        self.ending_point = ending_point
        self.data = data
        self.arrival_time = arrival_time
        self.booking = booking
        self.travel_time = travel_time




def calculate_dist_matrix(nodes_list):
    #TODO
    return generate_dist_matrix(len(nodes_list) * 2, 10)

# only for throuble shooting
def generate_dist_matrix(size, max_val):
    dist_matrix = []

    return dist_matrix

def calculate_pred_hash(nodes_list):
    nodes_list = list(nodes_list)
    pred_hash = {}
    for n in nodes_list:
        if(n.starting_point in pred_hash):
            pred_hash[n.starting_point].append(int(n.ending_point))
        else:
            pred_hash[n.starting_point] = [(int(n.ending_point))]
        if(n.ending_point not in pred_hash):
            pred_hash[n.ending_point] = []
    return pred_hash

'''def try_make_route_from_node(node):
    nodes_list = take_nodes_from_bd(7)
    nodes_list.append(node)
    dist_matrix = calculate_dist_matrix(nodes_list)
    print("************")
    print(dist_matrix)
    print("*********")
    pred_hash = calculate_pred_hash(nodes_list)

    with xmlrpc.client.ServerProxy("http://make-route-service:8000/") as proxy:
        print(pred_hash)
        result = proxy.calculate_route(dist_matrix, pred_hash, [], {})
        return result'''

