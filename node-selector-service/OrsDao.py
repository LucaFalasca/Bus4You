import requests

def getMatrix(nodes):
    url = 'http://ors-app:8080/ors/v2/matrix/driving-car'
    body = {}
    body['locations'] = nodes
    body['metrics'] = ['duration']
    
    data = requests.post(url, json = body).json()

    n_nodes = len(nodes)

    matrix = [[0 for j in range(n_nodes)] for i in range(n_nodes)]

    for i in range(n_nodes):
        for j in range(n_nodes):
            matrix[i][j] = data['durations'][i][j]

    print(matrix)
    return matrix

def test_vroom():
    url = 'http://vroom:3000/'
    body = {}
    body['vehicles'] = [{'id': 0, "capacity": [4], "profile": "driving-car", 'start': [12.527504,41.837339]}]
    body['shipments'] = [
    {
      "amount": [1],
      "pickup": {
        "id": 4,
        "service_after": [300],
        "location": [12.627504,41.837339]
      },
      "delivery": {
        "id": 3,
        "service": 300,
        "location": [12.427504,41.837339]
      }
    }
  ]
    body['options'] = {'g': True}
    
    data = requests.post(url, json = body).json()

    print(data)

    return data

class shipment:
    def __init__(self, amount, id_pickup, pickup, id_delivery, delivery, time_window):
        self.amount = amount
        self.id_pickup = id_pickup
        self.pickup = pickup
        self.id_delivery = id_delivery
        self.delivery = delivery 
        self.time_window = time_window

def make_route(bus_start_position, shipments):
    url = 'http://vroom:3000/'
    body = {}
    body['vehicles'] = [{'id': 0, "capacity": [8], "profile": "driving-car", 'start': bus_start_position}]
    body['shipments'] = []

    for shipment in shipments:
        s = {}
        s["amount"] = [shipment.amount]
        pickup = {}
        pickup["id"] = shipment.id_pickup
        if(shipment.time_window[0] != None):
            #pickup["service_at"] = [shipment.time_window[0]]
            pickup["time_windows"] = [[shipment.time_window[0], shipment.time_window[1]]]
        pickup["location"] = shipment.pickup
        s["pickup"] = pickup
        delivery = {}
        delivery["id"] = shipment.id_delivery
        if(shipment.time_window[1] != None):
            #delivery["service_at"] = [shipment.time_window[1]]
            delivery["time_windows"] = [[shipment.time_window[0], shipment.time_window[1]]]
        delivery["location"] = shipment.delivery
        s["delivery"] = delivery
        body['shipments'].append(s)

    body['options'] = {'g': True}

    print(body)

    data = requests.post(url, json = body).json()

    print(data)

    return data

def make_route_plan(bus_start_position, shipments):
    url = 'http://vroom:3000/'
    body = {}
    body['vehicles'] = [{'id': 0, "capacity": [8], "profile": "driving-car", 'start': bus_start_position}]
    body['shipments'] = []

    body["steps"] = [{
          "type": "start"
        },
        {
          "type": "pickup",
          "id": 1
        },
        {
          "type": "delivery",
          "id": 1
        },
        {
          "type": "pickup",
          "id": 3
        },
        {
          "type": "delivery",
          "id": 3
        },
        {
          "type": "pickup",
          "id": 5
        },
        {
          "type": "delivery",
          "id": 5
        },
        {
          "type": "end"
        }]
    

    for shipment in shipments:
        s = {}
        s["amount"] = [shipment.amount]
        pickup = {}
        pickup["id"] = shipment.id_pickup
        if(shipment.time_window[0] != None):
            #pickup["service_at"] = [shipment.time_window[0]]
            pickup["time_windows"] = [[shipment.time_window[0], shipment.time_window[1]]]
        pickup["location"] = shipment.pickup
        s["pickup"] = pickup
        delivery = {}
        delivery["id"] = shipment.id_delivery
        if(shipment.time_window[1] != None):
            #delivery["service_at"] = [shipment.time_window[1]]
            delivery["time_windows"] = [[shipment.time_window[0], shipment.time_window[1]]]
        delivery["location"] = shipment.delivery
        s["delivery"] = delivery
        body['shipments'].append(s)

    body['options'] = {'g': True, 'c': True}

    print(body)

    data = requests.post(url, json = body).json()

    print(data)

    return data

if __name__ == '__main__':
    getMatrix([[12.527504,41.837339],[12.627504,41.837339],[12.427504,41.837339],[12.527504,41.737339], [12.427504,41.737339]])
    #test_vroom()
    #test_opt()

    #s1 = shipment(1, 1, [12.627504,41.837339], 1, [12.427504,41.837339], [0, 1793])
    #s2 = shipment(1, 3, [12.627504,41.737339], 3, [12.527504,41.737339], [None, None])
    #s3 = shipment(1, 5, [12.627504,41.637339], 5, [12.527504,41.737339], [4355, 100000])
    #r1 = make_route(s1.pickup, [s1, s2, s3])
    #r2 = make_route(s2.pickup, [s1, s2, s3])
    #r3 = make_route(s3.pickup, [s1, s2, s3])

    #print("steps r1 " + str(r1["routes"][0]["steps"]))
    #print("steps r2 " + str(r2["routes"][0]["steps"]))
    #print("steps r3 " + str(r3["routes"][0]["steps"]))

    #print("cost r1 " + str(r1["summary"]["cost"]))
    #print("cost r2 " + str(r2["summary"]["cost"]))
    #print("cost r3 " + str(r3["summary"]["cost"]))
    #test_vroom()