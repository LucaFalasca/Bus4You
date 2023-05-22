import time

#from neo4j import GraphDatabase, basic_auth
import xmlrpc.server

from connect import create_person, create_stop, create_startStop, create_endStop
import random

class Neo4jMicroservice:

    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth, encrypted=False)
        self.driver.verify_connectivity()
        self.db = "neo4j"

    #Funzioni Dao

    #Aggiungi persona
    def insert_person(self, name):
        session = self.driver.session(database=self.db)
        session.execute_write(create_person, name)
        session.close()

    def insert_stop(self, name, hour, date):
        session = self.driver.session(database=self.db)
        session.execute_write(create_stop, name, hour, date)
        session.close()

    def insert_startStop(self, user, stop, hour, date):
        session = self.driver.session(database=self.db)
        session.execute_write(create_startStop, user, stop, hour, date)
        session.close()

    def insert_endStop(self, user, stop, hour, date):
        session = self.driver.session(database=self.db)
        session.execute_write(create_endStop, user, stop, hour, date)
        session.close()

    #L'esecuzione è un placeholder quindi alcuni dati non hanno un senso logico
    def insert_booking(self, user , starting_point , ending_point , data , arrival_time , travel_time):
            #self.insert_startStop(user, starting_point, arrival_time, data)
            #self.insert_endStop(user, ending_point, arrival_time+travel_time, data)
            return "ok"


def insert_booking(user , starting_point , ending_point , data , arrival_time , travel_time):
        return service.insert_booking(user , starting_point , ending_point , data , arrival_time , travel_time)


class Node:

    def __init__(self, starting_point, ending_point, data, arrival_time, travel_time):
        self.starting_point = starting_point
        self.ending_point = ending_point
        self.data = data
        self.arrival_time = arrival_time
        self.travel_time = travel_time

def take_nodes_from_bd(number_of_nodes):
    #TODO
    return [Node("0", "1", "11/05/2023", "13:45", "00:15"),
            Node("2", "3", "11/05/2023", "14:00", "00:40"),
            Node("4", "5", "11/05/2023", "14:15", "00:40"),
            Node("6", "7", "11/05/2023", "14:30", "00:40"),
            Node("8", "10", "11/05/2023", "14:45", "00:40"),
            Node("10", "11", "11/05/2023", "15:00", "00:15"),
            Node("10", "13", "11/05/2023", "15:15", "00:15")]

def calculate_initial_route(nodes_list):
    route = []
    for n in nodes_list:
        route.append(int(n.starting_point))
        route.append(int(n.ending_point))
    return route

def calculate_dist_matrix(nodes_list):
    #TODO
    return generate_dist_matrix(len(nodes_list) * 2, 10)

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

def calculate_pred_hash(nodes_list):
    nodes_list = list(nodes_list)
    pred_hash = {}
    for n in nodes_list:
        if(n.starting_point in pred_hash):
            pred_hash[n.starting_point].append(int(n.ending_point))
        else:
            pred_hash[n.starting_point] = [(int(n.ending_point))]
    return pred_hash

def try_make_route_from_node(node):
    nodes_list = take_nodes_from_bd(7)
    nodes_list.append(node)
    route = calculate_initial_route(nodes_list)
    dist_matrix = calculate_dist_matrix(nodes_list)
    pred_hash = calculate_pred_hash(nodes_list)
    with xmlrpc.client.ServerProxy("http://make-root-service:8000/") as proxy:
        print(route, dist_matrix, pred_hash)
        result = proxy.two_opt_multistart(route, dist_matrix, pred_hash, 10)
        return result
        


     
    

if __name__ == "__main__":
    
    print(try_make_route_from_node(Node("14", "15", "11/05/2023", "15:30", "00:15")))
    '''
    uri = "neo4j://neo4jDb:7687"
    auth=basic_auth("neo4j", "123456789")
    service = Neo4jMicroservice(uri, auth)
    service.insert_person("Luca")
    service.insert_stop("Tor Vergata (Medicina)", "13:45", "11/05/2023")
    service.insert_startStop("Luca", "Tor Vergata (Medicina)", "13:45", "11/05/2023")
    service.insert_endStop("Luca", "Anagnina", "14:00", "11/05/2023")
    service.insert_booking("Stefan", "Anagnina", "Tor Vergata", "12/05/2023", "14:00", "00:15")

    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    server.register_function(insert_booking, "insert_booking")
    server.serve_forever()

# Esempio di utilizzo
uri = "bolt://localhost:7687"
auth=("neo4j", "password")
service = Neo4jMicroservice(uri, auth)

service.insert_person("Luca")
service.insert_stop("Tor Vergata (Medicina)", "13:45", "11/05/2023")
service.insert_startStop("Luca", "Tor Vergata (Medicina)", "13:45", "11/05/2023")
service.insert_endStop("Luca", "Anagnina", "14:00", "11/05/2023")
service.insert_booking("Stefan", "Anagnina", "Tor Vergata", "12/05/2023", "14:00", "00:15")
'''