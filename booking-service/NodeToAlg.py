from Neo4jDAO import *
from Node import *

class NodeToAlg:

    def __init__(self, dao):
        self.dao = dao






    #La funzione restituisce una lista di nodi da Neo4J formattatta in modo da essere usata per l'algoritmo
    def take_nodes_from_bd(self, booking_id):
        nodes = self.dao.get_cluster_nodes(booking_id)
        # format nodes for algorithm
        str_nodes = []
        nodi = []
        for node in nodes:
            str_node = [str(elem) for elem in node]
            str_node[1] = str_node[1].split(':')[0] + ':' + str_node[1].split(':')[1]
            nodo = Node(str_node[3], str_node[4], str_node[2], str_node[1], str_node[0])
            nodi.append(nodo)
        return nodi

