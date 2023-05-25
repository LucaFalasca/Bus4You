import datetime
import time
import random
import requests
import json
import xmlrpc.server

from neo4j import GraphDatabase, basic_auth
from neo4j._spatial import  WGS84Point
from neo4J_dao import create_person, create_stop, create_startStop, create_endStop, create_travel, create_distances


#La funzione Prepara il drive di collegamento da cui si possono creare sessiono per accederci.
#NOTA I driver sono molto dispendiosi in risorse, farne UNO solo.
def setUpDriver():
    uri = "neo4j://neo4jDb:7687"
    auth=basic_auth("neo4j", "123456789")
    driver = GraphDatabase.driver(uri, auth=auth, encrypted=False)
    driver.verify_connectivity()
    return driver


#Lista di funzioni eseguibili esternamente
def insert_person(session, username):
    session.execute_write(create_person, username)

def insert_stop(session, name, hour, date, posX, posY):
    session.execute_write(create_stop, name, hour, date, posX, posY)

def insert_start_stop(session, user, stop, hour, date, position):
    session.execute_write(create_startStop, user, stop, hour, date, position)

def insert_end_stop(session, user, stop, hour, date, position):
    session.execute_write(create_endStop, user, stop, hour, date, position)

def insert_travel(session, starting_point, ending_point, start_time, arrival_time, day, travel_time):
    session.execute_write(create_travel, starting_point, ending_point, start_time, arrival_time, day, travel_time)

def insert_connection():
    session.execute_write(create_distances)

def insert_booking(user , starting_point , ending_point , data , arrival_time , travel_time, posX1, posY1, posX2, posY2):
    session = driver.session(database=db)
    pointStart = WGS84Point((posX1, posY1))
    pointEnd = WGS84Point((posX2, posY2))
    start_time = (datetime.datetime.combine(datetime.date.today(), arrival_time) - travel_time).time()
    insert_start_stop(session, user, starting_point, start_time, data, pointStart)
    insert_end_stop(session, user, ending_point, arrival_time, data, pointEnd)
    insert_travel(session, starting_point, ending_point, start_time, arrival_time, data, travel_time)
    session.close()
    return "ok" #Usa questo per verificare se legge la funzione


#La seguente funzione restituisce una terna di tre volori necessari per l'algoritmo
#1) Un dizionaro dove per chiave ha l'id effettivo della fermata del grafo e per valore il suo id nella matrice delle distanze e precedenza
#2) La matrice delle distanze (al momento spaziali)
#3) Il dizionario delle precedenze
#NOTA LA FUNZIONE NECESSITA DI ESSERE INVOCATA DOPO AVER COSTRUITO I NODI DI COLLEGAMENTO (make_connection)
def prepare_for_alg():
    session = driver.session(database=db)
    dizionario_fermate = {}
    matrice = []
    dizionario_precedenze = {}

    #Nel primo Step preparariamo il dizionario biettivo tra l'id della fermata nel Database e l'Algoritmo
    contatore = 1
    query = "MATCH (f:Fermata) RETURN id(f) AS id_fermata"
    result = session.run(query)
    for record in result:
        id_fermata = record["id_fermata"]
        dizionario_fermate[id_fermata] = contatore # aggiungere una nuova voce al dizionario con l'ID come chiave e il valore auto-incrementato come valore
        contatore += 1

    # stampare il dizionario risultante
    print("Dizionario Fermate: ")
    print(dizionario_fermate)
    print("********************")


    #Nel secondo step ci prepariamo la nostra matrice di distanze
    #Qui costruiamo la nostra matrice e inseriamo distanza 0 tra un nodo con stesso
    for i in range(len(dizionario_fermate)):
        matrice.append([])
        for j in range(len(dizionario_fermate)):
            matrice[i].append(0.0)

    #Ora andiamo a inserire tutte le distanze nella matrice
    result = session.run("MATCH (a)-[r:DISTANCE_TO]->(b) RETURN id(a) AS nodeA_id, id(b) AS nodeB_id, r.distance AS distance")
    for record in result:
        nodeA_id = record["nodeA_id"]
        nodeB_id = record["nodeB_id"]
        distance = record["distance"]
        matrice[dizionario_fermate[nodeA_id]-1][dizionario_fermate[nodeB_id]-1] = distance
        matrice[dizionario_fermate[nodeB_id]-1][dizionario_fermate[nodeA_id]-1] = distance
    print("Matrice distanze: ")
    print(matrice)
    print("********************")

    #Ora prepariamo il dizionario delle precedenze
    result = session.run("MATCH (a:Fermata)-[r:TRAVEL]->(b:Fermata) RETURN id(a) AS nodeA_id, id(b) AS nodeB_id")
    for record in result:
        nodeA_id = record["nodeA_id"]
        nodeB_id = record["nodeB_id"]
        dizionario_precedenze[dizionario_fermate[nodeA_id]] = dizionario_fermate[nodeB_id]
    print("Dizionario precedenze: ")
    print(dizionario_precedenze)
    print("********************")

    session.close()
    return dizionario_fermate, matrice, dizionario_precedenze





#Make Connection ha come compito quello di cercare tra i nodi del grafo quelli compatibili spazialmente
#E' una funziona del tutto autonoma è invocabile da altri microdervizi in qualunque momento
#Puo essere eseguita piu volte non crea doppie connessioni
#Al momento attuale crea un grafo ompleto con tutti i nodi
#
def make_connections():
    insert_connection() #inizialmente si calcola tutte le conessione e inserisce l arco di compatibilità tra due nodi solo se minore di un certo dato (il dato non è ancora stato inserito)


#Questa simulazioni simula una generazio di fermate con dati realistici
def generate_fermate(sizeUsers):

    nomi = ["Marco", "Giulia", "Matteo", "Francesca", "Luca", "Chiara", "Alessandro", "Valentina", "Davide", "Sara",
            "Simone", "Martina", "Lorenzo", "Elisa", "Giacomo", "Federica", "Andrea", "Alice", "Giovanni", "Beatrice",
            "Nicola", "Elena", "Riccardo", "Cristina", "Stefano", "Maria", "Antonio", "Laura", "Filippo", "Caterina"]

    fermate = [
        ["Termini", (41.9014, 12.5005)],
        ["Piazza Venezia", (41.8954, 12.4823)],
        ["Colosseo", (41.8902, 12.4923)],
        ["Circo Massimo", (41.8839, 12.4844)],
        ["Piazza Navona", (41.8992, 12.4736)],
        ["Campo de' Fiori", (41.8957, 12.4722)],
        ["Trastevere", (41.8896, 12.4673)],
        ["Piazza del Popolo", (41.9105, 12.4768)],
        ["Tiburtina", (41.9108, 12.5291)],
        ["San Giovanni", (41.8854, 12.5093)],
        ["Boccea", (41.9062, 12.3932)],
        ["Eur Fermi", (41.8282, 12.4641)],
        ["Flaminio", (41.9142, 12.4751)],
        ["Ostiense", (41.8759, 12.4803)],
        ["Viale Marconi", (41.8425, 12.4719)],
        ["Vittorio Emanuele", (41.8960, 12.5090)],
        ["Monte Mario", (41.9248, 12.4455)],
        ["Piazza Cavour", (41.9051, 12.4665)],
        ["Porta Maggiore", (41.8859, 12.5147)],
        ["Re di Roma", (41.8845, 12.5183)],
        ["Largo Argentina", (41.8956, 12.4764)],
        ["San Paolo", (41.8676, 12.4802)],
        ["Piramide", (41.8754, 12.4815)],
        ["San Lorenzo", (41.8979, 12.5207)],
        ["Ponte Milvio", (41.9327, 12.4750)],
        ["Colli Albani", (41.8694, 12.5339)],
        ["Aurelia", (41.9007, 12.4307)],
        ["Baldo degli Ubaldi", (41.9019, 12.4303)],
        ["San Pietro", (41.9022, 12.4549)],
        ["Porta Pia", (41.9082, 12.4989)]
    ]

    giorno = datetime.date(2023, 5, 18)
    ora_di_arrivo = datetime.time(13, 30, 0)

    tempo_impiegato = datetime.timedelta(minutes=15)  # la durata da aggiungere (15 min)


    random.seed(time.time())
    for i in range(sizeUsers):

        fermata1 = random.choice(fermate)
        fermata2 = random.choice(fermate)
        insert_booking(random.choice(nomi), fermata1[0], fermata2[0], giorno, ora_di_arrivo, tempo_impiegato, fermata1[1][0], fermata1[1][1], fermata2[1][0], fermata2[1][1])



if __name__ == "__main__":


    driver = setUpDriver()
    db = "neo4j"


    session = driver.session(database=db)
    generate_fermate(10) #Attenzione questa funzione crea nodi ogni volta che viene invocata, cancellare i volumi o commentarla per non ritrovarsi con grafo di 100 fermate
    make_connections()
    prepare_for_alg()




    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    server.register_function(insert_booking, "insert_booking")
    server.serve_forever()
    session.close()



