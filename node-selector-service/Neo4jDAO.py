from datetime import time, datetime
from datetime import time

from neo4j import GraphDatabase


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

    def create_booking_type_end(self, username, name_start_stop, name_end_stop, date, hour_end, position_start_stop,
                                position_end_stop):
        with self.driver.session() as session:
            result = session.run(
                "MERGE (b:Booking {name_start_stop: $name_start_stop, type: 'end', name_end_stop: $name_end_stop, date: $date,"
                "hour_end: $hour_end, position_start_stop: $position_start_stop,"
                "position_end_stop: $position_end_stop})"
                "RETURN id(b)",
                name_start_stop=name_start_stop, name_end_stop=name_end_stop, date=date,
                hour_end=hour_end, position_start_stop=position_start_stop, position_end_stop=position_end_stop
            )
            booking_id = result.single()[0]
        return booking_id

    def create_booking_type_start(self, it_id, username, name_start_stop, name_end_stop, date, hour_start,
                                  position_start_stop,
                                  position_end_stop):
        with self.driver.session() as session:
            result = session.run(
                "MERGE (b:Booking {name_start_stop: $name_start_stop, type: 'start', name_end_stop: $name_end_stop, date: $date,"
                "hour_start: $hour_start, position_start_stop: $position_start_stop,"
                "position_end_stop: $position_end_stop, it_id: $it_id })"
                "RETURN id(b)",
                name_start_stop=name_start_stop, name_end_stop=name_end_stop, date=date,
                hour_start=hour_start, position_start_stop=position_start_stop, position_end_stop=position_end_stop,
                it_id=it_id
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
                "MERGE (u)-[:BOOKS]->(b) "
                "MERGE (s1)-[:MUST_FOLLOW]->(s2)",
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

    def search_for_compatibility_type_1(self, booking_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Booking)-[:START_STOP]->(s:Stop) "
                "WHERE id(b) = $booking_id "
                "WITH s, b "
                "MATCH (other_stop:Stop)<-[:END_STOP]-(other_booking:Booking) "
                "WHERE id(other_booking) <> $booking_id AND b.date = other_booking.date "
                "WITH s, other_stop, point.distance(s.position, other_stop.position) AS distance, b, other_booking "
                "WHERE distance < 2500 AND NOT (b)-[:COMPATIBLE]-(other_booking) "
                "MERGE (b)-[r:COMPATIBLE {distance: distance, type: 1}]->(other_booking)",
                booking_id=booking_id
            )
            summary = result.consume()
            created = summary.counters.relationships_created
            if created > 0:
                return True
            else:
                return False

    def search_for_compatibility_type_2(self, booking_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Booking)-[:END_STOP]->(s:Stop) "
                "WHERE id(b) = $booking_id "
                "WITH s, b "
                "MATCH (other_stop:Stop)<-[:START_STOP]-(other_booking:Booking) "
                "WHERE id(other_booking) <> $booking_id AND b.date = other_booking.date "
                "WITH s, other_stop, point.distance(s.position, other_stop.position) AS distance, b, other_booking "
                "WHERE distance < 2500  AND NOT (b)-[:COMPATIBLE]-(other_booking) "
                "MERGE (b)-[r:COMPATIBLE {distance: distance, type: 2}]->(other_booking) ",
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
                    "date": datetime.strptime(record["date"], "%Y-%m-%d").date(),
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

    def get_random_booking_it_id(self):
        query = (
            "MATCH (b:Booking) "
            "WITH b, rand() AS r "
            "ORDER BY r "
            "LIMIT 1 "
            "RETURN b.it_id AS b_id"
        )

        with self.driver.session() as session:
            result = session.run(query)

            for record in result:
                # Restituzione dell'id del nodo Booking selezionato casualmente
                return record["b_id"]

    def get_random_booking(self):
        query = (
            "MATCH (b:Booking) "
            "WITH b, rand() AS r "
            "ORDER BY r "
            "LIMIT 1 "
            "RETURN id(b) AS b_id"
        )

        with self.driver.session() as session:
            result = session.run(query)

            for record in result:
                # Restituzione dell'id del nodo Booking selezionato casualmente
                return record["b_id"]

    def get_start_end_bookings_with_limit_stripped(self, booking_id, limit):
        query = (
            "MATCH (b:Booking)-[:COMPATIBLE*]-(booking:Booking) "
            "WHERE b.it_id = $booking_id "
            "WITH collect(DISTINCT b) + collect(DISTINCT booking) as all_bookings "
            "UNWIND all_bookings as booking "
            "MATCH (booking)<-[:BOOKS]-(u:User)"
            "RETURN DISTINCT id(booking) AS b_id, booking.hour_start AS b_hs, booking.hour_end AS b_he, booking.date AS b_day, "
            "booking.name_start_stop AS start_stop, "
            "booking.name_end_stop AS end_stop, booking.position_end_stop AS position_end_stop, "
            "booking.position_start_stop AS position_start_stop, booking.type AS b_type, booking.it_id as it_id, "
            "u.name as u_name LIMIT $limit"
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
            print(1)
            result = session.run(query, booking_id=booking_id, limit=limit)
            print(2)
            bookings = []
            for record in result:
                print(3)
                print(record)
                booking = {
                    "id": record["b_id"],
                    "date": record["b_day"],
                    "name_start_stop": record["start_stop"],
                    "name_end_stop": record["end_stop"],
                    "position_start_stop": record["position_start_stop"],
                    "position_end_stop": record["position_end_stop"],
                    "it_id": record["it_id"],
                    "user": record["user_name"],
                    "type": record["b_type"]
                }
                print(3.5)
                if record["b_type"] == "start":
                    booking["hour"] = (record["b_hs"], None)
                else:
                    booking["hour"] = (None, record["b_he"])
                    print(3.6)
                bookings.append(booking)
            print(4)
            # Consuma tutti i record prima di restituire il risultato
            result.consume()
            print(5)
        # Restituzione della lista di prenotazioni
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
                    "date": datetime.strptime(record["date"], "%Y-%m-%d").date(),
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

    def get_all_bookings(self):
        return self.get_start_end_bookings() + self.get_end_type_bookings()

    def delete_nodes_from_list(self, booking_ids):
        query = (
            "MATCH (b:Booking)-[r]-() "
            "WHERE id(b) in $booking_ids "
            "DETACH DELETE b, r"
        )
        with self.driver.session() as session:
            session.run(query, booking_ids=booking_ids)



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

    def get_cluster_nodes_json(self, booking_id):
        limit = 7  # Imposta il limite desiderato

        query = (
            "MATCH (startNode:Booking) "
            "WHERE startNode.it_id = $booking_id "
            "CALL apoc.path.spanningTree(startNode, { "
            "  relationshipFilter: 'COMPATIBLE', "
            "  labelFilter: 'Booking', "
            "  maxLevel: $limit, "
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
                booking_id = record["b_id"]
                compatible_bookings = session.run(
                    "MATCH (booking:Booking)-[:COMPATIBLE]-(other:Booking) "
                    "WHERE id(booking) = $booking_id "
                    "RETURN id(other) as other_id, other.it_id as other_it_id",
                    booking_id=booking_id
                )
                compatible_ids = [comp_record["other_it_id"] for comp_record in compatible_bookings]

                booking = {
                    "it_id": record["it_id"],
                    "id_neo4j": booking_id,
                    "date": record["b_day"],
                    "name_start_stop": record["start_stop"],
                    "name_end_stop": record["end_stop"],
                    "position_start_stop": str(record["position_start_stop"]),  # Converti in stringa
                    "position_end_stop": str(record["position_end_stop"]),  # Converti in stringa
                    "user": record["user_name"],
                    "type": record["b_type"],
                    "compatible_bookings": compatible_ids
                }

                if record["b_type"] == "start":
                    booking["hour"] = (record["b_hs"], "None")
                else:
                    booking["hour"] = ("None", record["b_he"])

                bookings.append(booking)

        return bookings

    def get_all_clusters_json(self):
        # Ottieni tutti gli it_id dai nodi Booking nel database
        with self.driver.session() as session:
            result = session.run("MATCH (b:Booking) RETURN b.it_id AS it_id")
            all_it_ids = [record["it_id"] for record in result]

        # Inizializza un dizionario vuoto per i cluster
        clusters = {}

        # Il cluster_id serve per identificare i diversi cluster
        cluster_id = 1

        while all_it_ids:
            # Preleva un it_id da all_it_ids
            it_id = all_it_ids.pop()

            # Ottieni il cluster per l'it_id corrente
            cluster = self.get_cluster_nodes_json(it_id)

            # Aggiungi il cluster al dizionario dei cluster
            clusters[f"cluster {cluster_id}"] = cluster

            # Incrementa l'identificativo del cluster
            cluster_id += 1

            # Rimuovi tutti gli it_id nel cluster corrente da all_it_ids
            cluster_it_ids = [booking["it_id"] for booking in cluster]
            all_it_ids = [it_id for it_id in all_it_ids if it_id not in cluster_it_ids]

        # Ritorna il dizionario dei cluster
        return clusters

    import json
    import random

    import json
    import random

    def get_random_cluster_json(self):
        # Ottieni un booking it_id casuale
        random_booking_it_id = self.get_random_booking_it_id()

        # Ottieni il cluster di nodi a partire dal booking it_id casuale
        cluster_nodes = self.get_cluster_nodes_json(random_booking_it_id)

        return cluster_nodes