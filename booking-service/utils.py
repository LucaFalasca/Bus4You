import csv
from lib2to3.pgen2 import driver
import datetime



def stampa_matrice(matrice):
    for riga in matrice:
        print(riga)

def real_get_all(driver):
    session = driver.session()
    result = session.run("MATCH (n:Fermata) RETURN n.name")

    for record in result:
        nomeFermata = record['n.name']
        print(nomeFermata)

    result.consume()  # consuma tutti i record
    session.close()  # chiudi la sessione solo dopo aver elaborato tutti i record

# Define a function to retrieve the id of a node with a specific label and property value
def print_node_info(label):
    with driver.session() as session:
        result = session.run("MATCH (n:{}) RETURN id(n) as node_id, n.name as name, n.date AS data_prenotazione, n.hour AS ora, n.position AS position".format(label))

        for record in result:
            data_prenotazione = record["data_prenotazione"]
            ora = record["ora"]
            ora_datetime = datetime.time(hour=ora.hour, minute=ora.minute, second=ora.second)
            position = record["position"]

            print(str(record["node_id"]) + " | " + record["name"] + " | " + data_prenotazione.strftime("%Y-%m-%d") + " | " + ora_datetime.strftime("%H:%M:%S") + " | " + "("+str(position.longitude)+","+str(position.latitude)+")")
    session.close()

def readStops():
    fermate = []

    # Apri il file di testo
    with open('stops.txt', 'r') as file:
    # Leggi il contenuto del file riga per riga
        lines = file.readlines()

    # Itera su ogni riga del file di testo
    for line in lines:
    # Divide la riga in una lista di valori usando il separatore ","
        values = line.strip().split(",")
        print(values)
    # Crea una tupla con le informazioni sulla fermata e aggiungila alla lista di fermate
        fermata = (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10])
        fermate.append(fermata)

    # Stampa la lista di fermate
    print(fermate)


"""
    url = "https://www.snap4city.org/superservicemap/api/v1/shortestpath?source=43.7767%3B11.2477&destination=43.7687%3B11.2620&routeType=car&startDatetime=2017-01-13T12%3A34%3A00&format=json"

    response = requests.get(url)
    data = json.loads(response.content)

    print(str(data["journey"]["routes"][0]["time"]))
"""

"""def prendi_chiavi_albero(attributo, data, path=[]):
        if isinstance(data, dict):
            for chiave in data:
                if chiave == attributo:
                    path.append(chiave)
                    print(".".join(path))
                    prendi_chiavi_albero(attributo, data[chiave], path)
                    path.pop()
                else:
                    path.append(chiave)
                    prendi_chiavi_albero(attributo, data[chiave], path)
                    path.pop()
        elif isinstance(data, list):
            for item in data:
                prendi_chiavi_albero(attributo, item, path)
"""
