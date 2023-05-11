from neo4j import GraphDatabase
import xmlrpc.server

from connect import create_person, create_stop, create_startStop, create_endStop


class Neo4jMicroservice:

    def __init__(self, uri, auth):
        #self.driver = GraphDatabase.driver(uri, auth=auth)
        #self.driver.verify_connectivity()
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

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    auth=("neo4j", "password")
    service = Neo4jMicroservice(uri, auth)

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
