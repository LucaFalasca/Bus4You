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
    body['vehicles'] = [{'id': 0, 'start': [12.527504,41.837339], 'end': [12.527504,41.837339]}]
    body['jobs'] = [{'id': 1, 'location': [12.627504,41.837339]}, {'id': 2, 'location': [12.427504,41.837339]}, {'id': 3, 'location': [12.527504,41.737339]}, {'id': 4, 'location': [12.427504,41.737339]}]
    body['options'] = {'g': True}
    
    data = requests.post(url, json = body).json()

    print(data)

    return data

if __name__ == '__main__':
    #getMatrix([[12.527504,41.837339],[12.627504,41.837339],[12.427504,41.837339],[12.527504,41.737339], [12.427504,41.737339]])
    test_vroom()