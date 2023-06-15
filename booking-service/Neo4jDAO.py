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

    def create_end_stop(self, name, position, hour_end):
        with self.driver.session() as session:
            result = session.run(
                "MERGE (n:Stop {name: $name , position: $position, hour_end: $hour_end})"
                "RETURN id(n)",
                name=name, position=position, hour_end=hour_end
            )
            stop_id = result.single()[0]
        return stop_id

    def create_booking(self, username, name_start_stop, name_end_stop, date, hour_end, position_start_stop,
                       position_end_stop):
        with self.driver.session() as session:
            result = session.run(
                "MERGE (b:Booking {name_start_stop: $name_start_stop, name_end_stop: $name_end_stop, date: $date,"
                "hour_end: $hour_end, position_start_stop: $position_start_stop,"
                "position_end_stop: $position_end_stop})"
                "RETURN id(b)",
                name_start_stop=name_start_stop, name_end_stop=name_end_stop, date=date,
                hour_end=hour_end, position_start_stop=position_start_stop, position_end_stop=position_end_stop
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