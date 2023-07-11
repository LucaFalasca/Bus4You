from Neo4jDAO_BS import *
from Node import *

class NodeToAlg:

    def __init__(self, dao):
        self.dao = dao






    #La funzione restituisce una lista di nodi da Neo4J formattatta in modo da essere usata per l'algoritmo
    def take_nodes_from_bd(self, booking_id, limit):
        return self.dao.get_start_end_bookings_with_limit(booking_id, limit)

