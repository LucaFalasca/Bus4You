from datetime import date
from datetime import time

from neo4j import GraphDatabase

from OrsDaoBS import *


class Neo4jDAO:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=False)
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def create_user(self, name):
        with self.driver.session() as session:
            result = session.run(
                "MERGE (u:User {name: $name})"
                "RETURN id(u)",
                name=name
            )
            user_id = result.single()[0]
        return user_id

    def create_stop(self, name, position):
        with self.driver.session() as session:
            result = session.run(
                "MERGE (n:Stop {name: $name , position: $position})"
                "RETURN id(n)",
                name=name, position=position
            )
            stop_id = result.single()[0]
        return stop_id

    def create_end_stop(self, name, position):
        with self.driver.session() as session:
            result = session.run(
                "MERGE (n:Stop {name: $name , position: $position})"
                "RETURN id(n)",
                name=name, position=position
            )
            stop_id = result.single()[0]
        return stop_id

    def create_booking_type_end(self, it_id, username, name_start_stop, name_end_stop, date, hour_end, position_start_stop,
                                position_end_stop):
        with self.driver.session() as session:
            result = session.run(
                "MERGE (b:Booking {name_start_stop: $name_start_stop, type: 'end', name_end_stop: $name_end_stop, date: $date,"
                "hour_end: $hour_end, position_start_stop: $position_start_stop,"
                "position_end_stop: $position_end_stop, it_id: $it_id})"
                "RETURN id(b)",
                name_start_stop=name_start_stop, name_end_stop=name_end_stop, date=date,
                hour_end=hour_end, position_start_stop=position_start_stop, position_end_stop=position_end_stop, it_id=it_id
            )
            booking_id = result.single()[0]
        return booking_id

    def create_booking_type_start(self, it_id, username, name_start_stop, name_end_stop, date, hour_start, position_start_stop,
                                position_end_stop):
        with self.driver.session() as session:
            result = session.run(
                "MERGE (b:Booking {name_start_stop: $name_start_stop, type: 'start', name_end_stop: $name_end_stop, date: $date,"
                "hour_start: $hour_start, position_start_stop: $position_start_stop,"
                "position_end_stop: $position_end_stop, it_id: $it_id })"
                "RETURN id(b)",
                name_start_stop=name_start_stop, name_end_stop=name_end_stop, date=date,
                hour_start=hour_start, position_start_stop=position_start_stop, position_end_stop=position_end_stop, it_id=it_id
            )
            booking_id = result.single()[0]
        return booking_id


    def connect_booking_to_stop(self, booking_id, username_id, start_stop_id, end_stop_id):
        with self.driver.session() as session:
            session.run(
                "MATCH (b:Booking), (s1:Stop), (s2:Stop), (u:User) "
                "WHERE id(b) = $booking_id AND id(s1) = $start_stop_id AND id(s2) = $end_stop_id AND "
                "id(u) = $username_id "
                "MERGE (b)-[:START_STOP]->(s1) "
                "MERGE (b)-[:END_STOP]->(s2) "
                "MERGE (u)-[:BOOKS]->(b) ",
                booking_id=booking_id, username_id=username_id, start_stop_id=start_stop_id, end_stop_id=end_stop_id
            )

    def get_all_stops(self):
        with self.driver.session() as session:
            result = session.run("MATCH (s:Stop) RETURN id(s) AS id_stop")
            stops = [record["id_stop"] for record in result]
        return stops



    def create_distances(self):
        return self.driver.session().run(
            "MATCH (a:Stop), (b:Stop) "
            "WHERE id(a) < id(b) "
            "MERGE (a)-[r:DISTANCE_TO]->(b) "
            "SET r.distance = point.distance(a.position,b.position) "
            "RETURN *"
        )

    def get_distances(self, stop_id_1, stop_id_2):
        result = self.driver.session().run(
            "MATCH (a:Stop), (b:Stop) "
            "WHERE id(a) = $stop_id_1 AND id(b) = $stop_id_2 "
            "RETURN toInteger(point.distance(a.position,b.position)) as distance",
            stop_id_1=stop_id_1, stop_id_2=stop_id_2
        )
        return result.single()["distance"]

    def search_for_compatibility_type_2(self, booking_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Booking)-[:START_STOP]->(s:Stop) "
                "WHERE id(b) = $booking_id "
                "WITH s, b "
                "MATCH (other_stop:Stop)<-[:END_STOP]-(other_booking:Booking) "
                "WHERE id(other_booking) <> $booking_id AND b.date = other_booking.date "
                "WITH s, other_stop, point.distance(s.position, other_stop.position) AS distance, b, other_booking "
                "WHERE distance < 2500 AND NOT (b)-[:COMPATIBLE]-(other_booking) "
                "MERGE (b)-[r:COMPATIBLE {distance: distance, type: 2}]->(other_booking)",
                booking_id=booking_id
            )
            summary = result.consume()
            created = summary.counters.relationships_created
            if created > 0:
                return True
            else:
                return False

    def search_for_compatibility_type_1(self, booking_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Booking)-[:END_STOP]->(s:Stop) "
                "WHERE id(b) = $booking_id "
                "WITH s, b "
                "MATCH (other_stop:Stop)<-[:START_STOP]-(other_booking:Booking) "
                "WHERE id(other_booking) <> $booking_id AND b.date = other_booking.date "
                "WITH s, other_stop, point.distance(s.position, other_stop.position) AS distance, b, other_booking "
                "WHERE distance < 2500  AND NOT (b)-[:COMPATIBLE]-(other_booking) "
                "MERGE (b)-[r:COMPATIBLE {distance: distance, type: 1}]->(other_booking) ",
                booking_id=booking_id
            )
            summary = result.consume()
            created = summary.counters.relationships_created
            if created > 0:
                return True
            else:
                return False

    def search_for_compatibility_type_3(self, booking_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Booking)-[:START_STOP]->(s:Stop) "
                "WHERE id(b) = $booking_id "
                "WITH s, b "
                "MATCH (other_stop:Stop)<-[:START_STOP]-(other_booking:Booking) "
                "WHERE id(other_booking) <> $booking_id AND b.date = other_booking.date "
                "WITH s, other_stop, point.distance(s.position, other_stop.position) AS distance, b, other_booking "
                "WHERE distance < 2500  AND NOT (b)-[:COMPATIBLE]-(other_booking) "
                "MERGE (b)-[r:COMPATIBLE {distance: distance, type: 3}]->(other_booking) ",
                booking_id=booking_id
            )
            summary = result.consume()
            created = summary.counters.relationships_created
            if created > 0:
                return True
            else:
                return False


    def get_cluster_nodes(self, booking_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Booking)-[:COMPATIBLE*]-(booking:Booking)-[:START_STOP]->(s1:Stop) "
                "WHERE id(b) = $booking_id "
                "WITH collect(DISTINCT booking) as all_bookings, s1 "
                "UNWIND all_bookings as booking "
                "MATCH (booking)-[:END_STOP]->(s2:Stop) "
                "RETURN id(booking), booking.hour_end, booking.date, id(s1), id(s2)",
                booking_id=booking_id
            )
            return [(record["id(booking)"], record["booking.hour_end"], record["booking.date"], record["id(s1)"], record["id(s2)"]) for record in result]



    def get_start_end_bookings(self):


        # Query per selezionare i nodi di tipo "Booking" con valore "start"
        query = (
            "MATCH (b:Booking) "
            "WHERE b.type = 'start' "
            "RETURN id(b) AS id, b.date AS date, b.hour_start AS hour_start, "
            "b.name_end_stop AS name_end_stop, b.name_start_stop AS name_start_stop, "
            "b.position_end_stop AS position_end_stop, b.position_start_stop AS position_start_stop, "
            "b.type AS type"
        )

        with self.driver.session() as session:
            # Esecuzione della query
            result = session.run(query)

            # Creazione della lista di dizionari con i risultati
            bookings = []
            for record in result:
                booking = {
                    "id": record["id"],
                    "date": date(record["date"].year, record["date"].month, record["date"].day),
                    "hour": (time(hour=record["hour_start"].hour, minute=record["hour_start"].minute), None),
                    "name_end_stop": record["name_end_stop"],
                    "name_start_stop": record["name_start_stop"],
                    "position_end_stop": record["position_end_stop"],
                    "position_start_stop": record["position_start_stop"],
                    "type": record["type"]
                }
                bookings.append(booking)

        # Chiusura della connessione al database e restituzione della lista di risultati
        session.close()
        return bookings


    def get_end_type_bookings(self):


        # Query per selezionare i nodi di tipo "Booking" con valore "start"
        query = (
            "MATCH (b:Booking) "
            "WHERE b.type = 'end' "
            "RETURN id(b) AS id, b.date AS date, b.hour_end AS hour_end, "
            "b.name_end_stop AS name_end_stop, b.name_start_stop AS name_start_stop, "
            "b.position_end_stop AS position_end_stop, b.position_start_stop AS position_start_stop, "
            "b.type AS type"
        )

        with self.driver.session() as session:
            # Esecuzione della query
            result = session.run(query)

            # Creazione della lista di dizionari con i risultati
            bookings = []
            for record in result:
                booking = {
                    "id": record["id"],
                    "date": date(record["date"].year, record["date"].month, record["date"].day),
                    "hour": (None, time(hour=record["hour_end"].hour, minute=record["hour_end"].minute)),
                    "name_end_stop": record["name_end_stop"],
                    "name_start_stop": record["name_start_stop"],
                    "position_end_stop": record["position_end_stop"],
                    "position_start_stop": record["position_start_stop"],
                    "type": record["type"]
                }
                bookings.append(booking)

        # Chiusura della connessione al database e restituzione della lista di risultati
        session.close()
        return bookings



    #Chiedere se aggiungere comunque gli stop_id per le API
    def get_start_end_bookings_with_limit(self, booking_id, limit):
        query = (
            "MATCH (startNode:Booking) "
            "WHERE id(startNode) = $booking_id "
            "CALL apoc.path.spanningTree(startNode, { "
            "  relationshipFilter: 'COMPATIBLE', "
            "  labelFilter: 'Booking', "
            " maxLevel: $limit, "
            "  limit: $limit "
            "}) "
            "YIELD path "
            "UNWIND nodes(path) AS bookingNode "
            "OPTIONAL MATCH (bookingNode)<-[:BOOKS]-(user:User) "
            "RETURN DISTINCT id(bookingNode) AS b_id, bookingNode.hour_start AS b_hs, bookingNode.hour_end AS b_he, "
            "bookingNode.date AS b_day, bookingNode.name_start_stop AS start_stop, bookingNode.name_end_stop AS end_stop, "
            "bookingNode.position_end_stop AS position_end_stop, bookingNode.position_start_stop AS position_start_stop, "
            "bookingNode.type AS b_type, bookingNode.it_id AS it_id, user.name AS user_name"
                )

        with self.driver.session() as session:
            result = session.run(query, booking_id=booking_id, limit=limit)

            bookings = []
            for record in result:
                booking = {
                    "id": record["b_id"],
                    "date": record["b_day"],
                    "name_start_stop": record["start_stop"],
                    "name_end_stop": record["end_stop"],
                    "position_start_stop": record["position_start_stop"],
                    "position_end_stop": record["position_end_stop"],
                    "type": record["b_type"]
                }
                if record["b_type"] == "start":
                    booking["hour"] = (record["b_hs"], None)
                else:
                    booking["hour"] = (None, record["b_he"])
                bookings.append(booking)

            # Consuma tutti i record prima di restituire il risultato
            result.consume()
        # Restituzione della lista di prenotazioni
        return bookings





    def get_all_bookings(self):
        return self.get_start_end_bookings() + self.get_end_type_bookings()

    '''def get_compatible_time_bookings(self, booking_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Booking)-[r:COMPATIBLE]->(other_booking:Booking) "
                "WHERE id(b) = $booking_id "
                "RETURN id(b) AS id, b.type AS type, b.hour_start AS hour_start, b.hour_end AS hour_end, "
                "b.position_start_stop AS position_start_stop, b.position_end_stop AS position_end_stop, "
                "id(other_booking) AS other_id, other_booking.type AS other_type, "
                "other_booking.hour_start AS other_hour_start, other_booking.hour_end AS other_hour_end, "
                "other_booking.position_start_stop AS other_position_start_stop, "
                "other_booking.position_end_stop AS other_position_end_stop, "
                "r.type_spatial AS type_spatial", booking_id = booking_id
            )
            nodes = []
            for record in result:
                node = {
                    "id": record["id"],
                    "type_spatial": record["type_spatial"],
                    "type": record["type"],
                    "hour_start": record["hour_start"],
                    "hour_end": record["hour_end"],
                    "position_start_stop": [record["position_start_stop"].latitude,
                                            record["position_start_stop"].longitude],
                    "position_end_stop": [record["position_end_stop"].latitude, record["position_end_stop"].longitude],
                    "other_id": record["other_id"],
                    "other_type": record["other_type"],
                    "other_hour_start": record["other_hour_start"],
                    "other_hour_end": record["other_hour_end"],
                    "other_position_start_stop": [record["other_position_start_stop"].latitude,
                                                  record["other_position_start_stop"].longitude],
                    "other_position_end_stop": [record["other_position_end_stop"].latitude,
                                                record["other_position_end_stop"].longitude]
                }
                nodes.append(node)

            for node in nodes:
                if node["type"] == "start" and node["other_type"] == "start":
                    hour = getMatrix([[node["position_start_stop"][0], node["position_start_stop"][1]],
                                      [node["other_position_start_stop"][0], node["other_position_start_stop"][1]]])[0][
                        1]

                    offset1 = max(5, 0.15 * hour)
                    offset2 = max(10, 0.3 * hour)

                    hour_diff = abs(
                        (int(node["hour_start"].split(":")[0]) * 60 + int(node["hour_start"].split(":")[1])) -
                        (int(node["other_hour_start"].split(":")[0]) * 60 + int(
                            node["other_hour_start"].split(":")[1])))

                    
                    print(offset1)
                    print(offset2)
                    print(hour)
                    print(hour_diff)
                    print(f"{hour - offset1} < {hour_diff} < {hour + offset2}")
                    

                    if not (hour - offset1 <= hour_diff <= hour + offset2):
                        session.run("MATCH (b:Booking)-[r:COMPATIBLE]->(other_booking:Booking) "
                                    "WHERE id(b) = $id AND id(other_booking) = $other_id "
                                    "DELETE r", id=node["id"], other_id=node["other_id"])

                if node["type"] == "end" and node["other_type"] == "start":
                    hour = getMatrix([[node["position_start_stop"][0], node["position_start_stop"][1]],
                                      [node["other_position_end_stop"][0], node["other_position_end_stop"][1]]])[0][
                        1]
                    offset1 = max(5, 0.15 * hour)
                    offset2 = max(10, 0.3 * hour)

                    hour_diff = abs(
                        (int(node["other_hour_start"].split(":")[0]) * 60 + int(node["other_hour_start"].split(":")[1])) -
                        (int(node["hour_end"].split(":")[0]) * 60 + int(
                             node["hour_end"].split(":")[1])))
                    
                    print(offset1)
                    print(offset2)
                    print(hour)
                    print(hour_diff)
                    print(f"{hour - offset1} < {hour_diff} < {hour + offset2}")
                    

                    if not (hour - offset1 <= hour_diff <= hour + offset2):
                        session.run("MATCH (b:Booking)-[r:COMPATIBLE]->(other_booking:Booking) "
                                    "WHERE id(b) = $id AND id(other_booking) = $other_id "
                                    "DELETE r", id=node["id"], other_id=node["other_id"])

                if node["type"] == "end" and node["other_type"] == "end":
                    matrix = getMatrix([[node["position_end_stop"][0], node["position_end_stop"][1]],
                                        [node["other_position_start_stop"][0], node["other_position_start_stop"][1]],
                                        [node["other_position_end_stop"][0], node["other_position_end_stop"][1]]])

                    hour_step1 = matrix[0][1]
                    hour_step2 = matrix[1][2]
                    hour = hour_step1 + hour_step2

                    offset1 = max(5, 0.15 * hour)
                    offset2 = max(10, 0.3 * hour)

                    hour_diff = abs(
                        (int(node["hour_end"].split(":")[0]) * 60 + int(node["hour_end"].split(":")[1])) -
                        (int(node["other_hour_end"].split(":")[0]) * 60 + int(
                            node["other_hour_end"].split(":")[1])))

                    print("facciamo delle prove...")
                    print(offset1)
                    print(offset2)
                    print(hour)
                    print(hour_diff)
                    print(f"{hour - offset1} < {hour_diff} < {hour + offset2}")


                    if not (hour - offset1 <= hour_diff <= hour + offset2):
                        session.run("MATCH (b:Booking)-[r:COMPATIBLE]->(other_booking:Booking) "
                                    "WHERE id(b) = $id AND id(other_booking) = $other_id "
                                    "DELETE r", id=node["id"], other_id=node["other_id"])

                if node["type"] == "start" and node["other_type"] == "end":
                    matrix = getMatrix([[node["position_start_stop"][0], node["position_start_stop"][1]],
                                        [node["position_end_stop"][0], node["position_end_stop"][1]],
                                        [node["other_position_start_stop"][0], node["other_position_start_stop"][1]],
                                        [node["other_position_end_stop"][0], node["other_position_end_stop"][1]]])

                    hour_step1 = matrix[0][1]
                    hour_step2 = matrix[1][2]
                    hour_step3 = matrix[2][3]
                    hour = hour_step1 + hour_step2 + hour_step3

                    offset1 = max(5, 0.15 * hour)
                    offset2 = max(10, 0.3 * hour)

                    hour_diff = abs(
                        (int(node["hour_start"].split(":")[0]) * 60 + int(node["hour_start"].split(":")[1])) -
                        (int(node["other_hour_end"].split(":")[0]) * 60 + int(
                            node["other_hour_end"].split(":")[1])))
                    
                    print(offset1)
                    print(offset2)
                    print(hour)
                    print(hour_diff)
                    print(f"{hour - offset1} < {hour_diff} < {hour + offset2}")
                    


                    if not (hour - offset1 <= hour_diff <= hour + offset2):
                        session.run("MATCH (b:Booking)-[r:COMPATIBLE]->(other_booking:Booking) "
                                    "WHERE id(b) = $id AND id(other_booking) = $other_id "
                                    "DELETE r", id=node["id"], other_id=node["other_id"])'''

    def get_compatible_time_bookings(self, booking_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Booking)-[r:COMPATIBLE]->(other_booking:Booking) "
                "WHERE id(b) = $booking_id "
                "RETURN id(b) AS id, b.type AS type, b.hour_start AS hour_start, b.hour_end AS hour_end, "
                "b.position_start_stop AS position_start_stop, b.position_end_stop AS position_end_stop, "
                "id(other_booking) AS other_id, other_booking.type AS other_type, "
                "other_booking.hour_start AS other_hour_start, other_booking.hour_end AS other_hour_end, "
                "other_booking.position_start_stop AS other_position_start_stop, "
                "other_booking.position_end_stop AS other_position_end_stop, "
                "r.type AS type_spatial", booking_id = booking_id
            )
            nodes = []

            for record in result:
                node = {
                    "id": record["id"],
                    "type_spatial": record["type_spatial"],
                    "type": record["type"],
                    "hour_start": record["hour_start"],
                    "hour_end": record["hour_end"],
                    "position_start_stop": [record["position_start_stop"].latitude,
                                            record["position_start_stop"].longitude],
                    "position_end_stop": [record["position_end_stop"].latitude, record["position_end_stop"].longitude],
                    "other_id": record["other_id"],
                    "other_type": record["other_type"],
                    "other_hour_start": record["other_hour_start"],
                    "other_hour_end": record["other_hour_end"],
                    "other_position_start_stop": [record["other_position_start_stop"].latitude,
                                                  record["other_position_start_stop"].longitude],
                    "other_position_end_stop": [record["other_position_end_stop"].latitude,
                                                record["other_position_end_stop"].longitude]
                }
                nodes.append(node)

            for node in nodes:
                hour_node1 = 0
                hour_node2 = 0
                matrix = getMatrix([[node["position_start_stop"][0], node["position_start_stop"][1]],
                                    [node["position_end_stop"][0], node["position_end_stop"][1]],
                                    [node["other_position_start_stop"][0], node["other_position_start_stop"][1]],
                                    [node["other_position_end_stop"][0], node["other_position_end_stop"][1]]])
                #TYPE 1
                if (node["type_spatial"] == 1):
                    print("OIIIIIIIIIIIIII")
                    if (node["type"] == "start"): hour_node1 = (int(node["hour_start"].split(":")[0]) * 60 + int(node["hour_start"].split(":")[1])) + matrix[0][1]
                    if (node["type"] == "end"):  hour_node1 = (int(node["hour_end"].split(":")[0]) * 60 + int(node["hour_end"].split(":")[1]))
                    if (node["other_type"] == "end"): hour_node2 = (int(node["other_hour_end"].split(":")[0]) * 60 + int(node["other_hour_end"].split(":")[1])) - matrix[3][2]
                    if (node["other_type"] == "start"): hour_node2 = (int(node["other_hour_start"].split(":")[0]) * 60 + int(node["other_hour_start"].split(":")[1]))


                    time_to_travel = abs(hour_node1 - hour_node2)
                    time_to_travel_ors = matrix[0][3]
                    offset1 = max(5, 0.15 * time_to_travel_ors)
                    offset2 = max(10, 0.3 * time_to_travel_ors)

                    print("-----------------")
                    print("Hour Start: " + str(hour_node1))
                    print("Hour End: " + str(hour_node2))
                    print(f"{time_to_travel_ors - offset1} < {time_to_travel} < {time_to_travel_ors + offset2}")
                    print("-----------------")

                    if not (time_to_travel_ors - offset1 <= time_to_travel <= time_to_travel_ors + offset2):
                        session.run("MATCH (b:Booking)-[r:COMPATIBLE]->(other_booking:Booking) "
                                    "WHERE id(b) = $id AND id(other_booking) = $other_id "
                                    "DELETE r", id=node["id"], other_id=node["other_id"])
                #TYPE 2
                if(node["type_spatial"] == 2):

                    print("Pronto 1 ?")
                    if (node["type"] == "start"):
                        hour_node1 = (int(node["hour_start"].split(":")[0]) * 60 + int(node["hour_start"].split(":")[1]))
                        print("Pronto 2 ?")
                    if (node["type"] == "end"):
                        hour_node1 = (int(node["hour_end"].split(":")[0]) * 60 + int(node["hour_end"].split(":")[1])) - matrix[0][1]
                        print("Pronto 3 ?")
                    if (node["other_type"] == "end"):
                        hour_node2 = (int(node["other_hour_end"].split(":")[0]) * 60 + int(node["other_hour_end"].split(":")[1]))
                        print("Pronto 4 ?")
                    if (node["other_type"] == "start"):
                        print("Pronto 4.5 ?")
                        print(node)
                        hour_node2 = (int(node["other_hour_start"].split(":")[0]) * 60 + int(node["other_hour_start"].split(":")[1])) + matrix[3][2]
                        print("Pronto 5 ?")

                    print("Pronto 6 ?")
                    print("Hour Start: " + str(hour_node1))
                    print("Hour End: " + str(hour_node2))
                    time_to_travel = abs(hour_node1 - hour_node2)
                    time_to_travel_ors = matrix[0][3]
                    offset1 = max(5, 0.15 * time_to_travel_ors)
                    offset2 = max(10, 0.3 * time_to_travel_ors)



                    print("-----------------")
                    print("Hour Start: " + str(hour_node1))
                    print("Hour End: " + str(hour_node2))
                    print(f"{time_to_travel_ors - offset1} < {time_to_travel} < {time_to_travel_ors + offset2}")
                    print("-----------------")

                    if not (time_to_travel_ors - offset1 <= time_to_travel <= time_to_travel_ors + offset2):
                        session.run("MATCH (b:Booking)-[r:COMPATIBLE]->(other_booking:Booking) "
                                    "WHERE id(b) = $id AND id(other_booking) = $other_id "
                                    "DELETE r", id=node["id"], other_id=node["other_id"])

                 # TYPE 3
                if (node["type_spatial"] == 3):
                    if (node["type"] == "start"): hour_node1 = (int(node["hour_start"].split(":")[0]) * 60 + int(node["hour_start"].split(":")[1]))
                    if (node["type"] == "end"):  hour_node1 = (int(node["hour_end"].split(":")[0]) * 60 + int(node["hour_end"].split(":")[1])) - matrix[1][0]
                    if (node["other_type"] == "end"): hour_node2 = (int(node["other_hour_end"].split(":")[0]) * 60 + int(node["other_hour_end"].split(":")[1])) - matrix[3][2]
                    if (node["other_type"] == "start"): hour_node2 = (int(node["other_hour_start"].split(":")[0]) * 60 + int(node["other_hour_start"].split(":")[1]))

                    time_to_travel = abs(hour_node1 - hour_node2)
                    time_to_travel_ors = matrix[0][2]
                    offset1 = max(5, 0.15 * time_to_travel_ors)
                    offset2 = max(10, 0.3 * time_to_travel_ors)

                    print("-----------------")
                    print("Hour Start: " + str(hour_node1))
                    print("Hour End: " + str(hour_node2))
                    print(f"{time_to_travel_ors - offset1} < {time_to_travel} < {time_to_travel_ors + offset2}")
                    print("-----------------")

                    if not (time_to_travel_ors - offset1 <= time_to_travel <= time_to_travel_ors + offset2):
                        session.run("MATCH (b:Booking)-[r:COMPATIBLE]->(other_booking:Booking) "
                                    "WHERE id(b) = $id AND id(other_booking) = $other_id "
                                    "DELETE r", id=node["id"], other_id=node["other_id"])


    '''def get_person_by_name(self, name):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Person {name: $name}) RETURN p", name=name)
            return result.single()["p"] if result.single() else None

    def create_person(self, name, age):
        with self.driver.session() as session:
            session.run("CREATE (p:Person {name: $name, age: $age})", name=name, age=age)

    def update_person_age(self, name, age):
        with self.driver.session() as session:
            session.run("MATCH (p:Person {name: $name}) SET p.age = $age", name=name, age=age)

    def delete_person_by_name(self, name):
        with self.driver.session() as session:
            session.run("MATCH (p:Person {name: $name}) DELETE p", name=name)'''