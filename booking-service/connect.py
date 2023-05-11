
#FUNZIONI

#Crea nodo Persona
def create_person(tx, name):
    return tx.run(
        "MERGE (p:Person {name: $name})",
        name=name
    )

#Crea nodo Fermata
def create_stop(tx, name, hour, date):
    return tx.run(
        "MERGE (n:Fermata {name: $name , hour: $hour , date: $date})",
        name=name, hour=hour, date=date
    )

#Crea arco fermataPartenza
def create_startStop(tx, nameUser, nameStop, hour, date):
    return tx.run(
        "MERGE (p:Person {name: $nameUser}) MERGE (f:Fermata {name: $nameStop , hour:$hour , date: $date }) MERGE (p)-[:START_STOP]->(f)",
        nameUser=nameUser, nameStop=nameStop,  hour=hour, date=date
    )

#Crea arco fermataArrivo
def create_endStop(tx, nameUser, nameStop, hour, date):
    return tx.run(
        "MERGE (p:Person {name: $nameUser}) MERGE (f:Fermata {name: $nameStop , hour:$hour , date: $date }) MERGE (p)-[:END_STOP]->(f)",
        nameUser=nameUser, nameStop=nameStop,  hour=hour, date=date
    )


#conex
#driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
#driver.verify_connectivity()


#Iniziamo a lavorare
#session = driver.session(database="neo4j")
#session.execute_write(create_person, name="Michael")
#session.execute_write(create_stop, name="Tor Vergata", position=3, hour="13:45", date="16/03/2023")
#session.execute_write(create_startStop, nameUser="Stefan", nameStop="Tor Vergata", hour="13:00", date="12/05/2023")
#session.execute_write(create_endStop, nameUser="Stefan", nameStop="Anagnina", hour="13:15", date="12/05/2023")
#session.close()