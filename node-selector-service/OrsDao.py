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
        "service": 300,
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

def test_opt():

    body = {"jobs":[{"id":1,"service":300,"amount":[1],"location":[1.98465,48.70329],"skills":[1],"time_windows":[[32400,36000]]},{"id":2,"service":300,"amount":[1],"location":[2.03655,48.61128],"skills":[1]},{"id":3,"service":300,"amount":[1],"location":[2.39719,49.07611],"skills":[2]},{"id":4,"service":300,"amount":[1],"location":[2.41808,49.22619],"skills":[2]},{"id":5,"service":300,"amount":[1],"location":[2.28325,48.5958],"skills":[14]},{"id":6,"service":300,"amount":[1],"location":[2.89357,48.90736],"skills":[14]}],"vehicles":[{"id":1,"profile":"driving-car","start":[2.35044,48.71764],"end":[2.35044,48.71764],"capacity":[4],"skills":[1,14],"time_window":[28800,43200]},{"id":2,"profile":"driving-car","start":[2.35044,48.71764],"end":[2.35044,48.71764],"capacity":[4],"skills":[2,14],"time_window":[28800,43200]}]}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': 'your-api-key',
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://api.openrouteservice.org/optimization', json=body, headers=headers)

    print(call.status_code, call.reason)
    print(call.text)

if __name__ == '__main__':
    #getMatrix([[12.527504,41.837339],[12.627504,41.837339],[12.427504,41.837339],[12.527504,41.737339], [12.427504,41.737339]])
    test_vroom()
    #test_opt()