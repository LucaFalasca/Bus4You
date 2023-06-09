import datetime
import time

import random
import requests
import json
import xmlrpc.server

from neo4j import GraphDatabase, basic_auth
from neo4j._spatial import  WGS84Point
from neo4J_dao import create_person, create_stop, create_startStop, create_endStop, create_travel, create_distances
from Neo4jDAO import *
from utils import *


#Usare questa funzione per generare un insieme di prenotazioni con dati realistici
def generate_stops(sizeUsers):

    users = ["Marco", "Giulia", "Matteo", "Francesca", "Luca", "Chiara", "Alessandro", "Valentina", "Davide", "Sara",
            "Simone", "Martina", "Lorenzo", "Elisa", "Giacomo", "Federica", "Andrea", "Alice", "Giovanni", "Beatrice",
            "Nicola", "Elena", "Riccardo", "Cristina", "Stefano", "Maria", "Antonio", "Laura", "Filippo", "Caterina"]

    stops = [
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

    day = datetime.date(2023, 5, 18)
    hour_end = datetime.time(13, 30, 0)


    random.seed(time.time())
    for i in range(sizeUsers):

        stop1 = random.choice(stops)
        stop2 = random.choice(stops)
        create_booking(random.choice(users), stop1[0], stop2[0], day, hour_end, stop1[1][0], stop1[1][1], stop2[1][0], stop2[1][1])



def create_booking(username, name_start_stop, name_end_stop, date, hour_end,
                   position_start_stop_X, position_start_stop_Y, position_end_stop_X, position_end_stop_Y):

    position_start_stop = WGS84Point((position_start_stop_X, position_start_stop_Y))
    position_end_stop = WGS84Point((position_end_stop_X, position_end_stop_Y))


    #get ID's, and create if not exists
    user_id = dao.create_user(username)
    stop_id_1 = dao.create_stop(name_start_stop, position_start_stop)
    stop_id_2 = dao.create_end_stop(name_end_stop, position_end_stop,hour_end)
    booking_id = dao.create_booking(username, name_start_stop, name_end_stop, date, hour_end,
                                    position_start_stop, position_end_stop)
    dao.connect_booking_to_stop(booking_id, user_id, stop_id_1, stop_id_2)


     
    

if __name__ == "__main__":


    dao = Neo4jDAO("neo4j://neo4jDb:7687", "neo4j", "123456789")
    create_booking("Stefan", "Termini", "Piazza Venezia", datetime.date(2023, 5, 18), datetime.time(13, 30, 0),
                41.9014, 12.5005, 41.8954, 12.4823)

    create_booking("Luca", "Colosseo", "Monte Mario", datetime.date(2023, 5, 18), datetime.time(14, 30, 0),
                   41.8902, 12.4923, 41.9248, 12.4455)
    #generate_stops(10)


    dao.close()

    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    #server.register_function(insert_booking, "insert_booking")
    server.serve_forever()
    #session.close()



