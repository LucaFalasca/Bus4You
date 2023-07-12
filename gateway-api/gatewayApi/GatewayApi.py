from flask import Flask, json, request
import xmlrpc.client
import random
import time
import requests

api = Flask(__name__)


@api.route('/api/login', methods=['GET'])
def login():
    mail = request.args.get('usr')
    password = request.args.get('pwd')
    with xmlrpc.client.ServerProxy("http://login-service:8000/") as proxy:
        result = proxy.rpc_login(mail, password)
        return json.dumps(result)


@api.route('/api/sign-up', methods=['GET'])
def signUp():
    name = request.args.get('name')
    surname = request.args.get('surname')
    mail = request.args.get('mail')
    password = request.args.get('pwd')
    birthdate = request.args.get('birthdate')
    username = request.args.get('usr')
    with xmlrpc.client.ServerProxy("http://login-service:8000/") as proxy:
        result = proxy.rpc_sign_up(name, surname, mail, password, birthdate, username)
        return json.dumps(result)


@api.route('/api/route-from-map', methods=['GET'])
def route_from_map():
    print("Ciao come va?")
    user = request.args.get('user')
    starting_point = request.args.get('starting_point')
    start_lat = request.args.get('start_lat')
    start_lng = request.args.get('start_lng')
    ending_point = request.args.get('ending_point')
    end_lat = request.args.get('end_lat')
    end_lng = request.args.get('end_lng')
    date = request.args.get('date')
    start_or_finish = request.args.get('start-finish')
    print("SOF" + start_or_finish)
    time = request.args.get('time')
    print(user, starting_point, ending_point, date, start_or_finish, time, start_lat, start_lng, end_lat, end_lng)
    with xmlrpc.client.ServerProxy("http://booking_service:8000/") as proxy:
        print("PROXY")
        result = proxy.insert_booking(user, starting_point, start_lat, start_lng, ending_point, end_lat, end_lng, date,
                                      start_or_finish, time)
        print(result)
        return json.dumps(result)


def generate_dist_matrix(size, max_val):
    random.seed(time.time())
    dist_matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(0)
            else:
                val = random.randint(1, max_val)
                row.append(val)
        dist_matrix.append(row)
    return dist_matrix


@api.route('/api/load_user_routes', methods=['GET'])
def load_user_routes():
    mail = request.args.get('mail')
    ret = []
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        user_routes = json.loads(proxy.get_user_routes(mail))
    for route in user_routes:
        ret.append({"it_cost": route[0], "it_prop_start": route[1], "it_prop_end": route[2], "it_status": route[3],
                    "route_past": route[4], "route_status": route[5], "route_expire": route[6], "start_stop": route[7],
                    "end_stop": route[8], "it_id": route[9]})

    return json.dumps(ret)


@api.route('/api/get_bus_stops', methods=['GET'])
def get_bus_stops():
    ret = []
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        bus_stops = json.loads(proxy.get_stops())
    for elem in bus_stops:
        stop = {"name": elem[0], "lat": elem[1], "lang": elem[2]}
        ret.append(stop)
    return json.dumps(ret)


@api.route('/api/get_bus_stops_rect', methods=['GET'])
def get_bus_stops_rect():
    ret = []
    x = request.args.get('x')
    y = request.args.get('y')
    height = request.args.get('height')
    width = request.args.get('width')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        bus_stops = json.loads(proxy.get_stops_rect(x, y, height, width))
    for elem in bus_stops:
        stop = {"name": elem[0], "lat": elem[1], "lang": elem[2]}
        ret.append(stop)
    return json.dumps(ret)


@api.route('/api/get_path', methods=['POST'])
def get_path():
    data = request.get_json()
    print(data)
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.get_stops_from_it(data)
        print(ret)
        stops = json.loads(ret)
    url = 'http://ors-app:8080/ors/v2/directions/driving-car/geojson'
    body = {}
    print(stops)
    true_stops = [[float(s[2]), float(s[1])] for s in stops]
    body['coordinates'] = true_stops
    
    print("CIAOO")
    print(body)
    result = requests.post(url, json=body).json()
    print(result)
    coords = result["features"][0]["geometry"]["coordinates"]
    print(coords)
    coords_reversed = [coord[::-1] for coord in coords]
    final_ret = {"coordinates": coords_reversed, "stops": true_stops}
    return json.dumps(final_ret)


@api.route('/api/confirm_it', methods=['GET'])
def confirm_it():
    it_id = request.args.get('it_id')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.confirm_it(it_id)
        #print(ret)
        return json.dumps(ret)


@api.route('/api/reject_it', methods=['GET'])
def reject_it():
    it_id = request.args.get('it_id')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.reject_it(it_id)
        #print(ret)
        return json.dumps(ret)


@api.route('/api/get_retry_info', methods=['GET'])
def get_retry_info():
    it_id = request.args.get('it_id')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.get_retry_info(it_id)
        #print(ret)
        return json.dumps(ret)


@api.route('/api/get_user_balance', methods=['GET'])
def get_user_balance():
    mail = request.args.get('user')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.get_user_balance(mail)
        #print("Gateway balance",ret)
        return json.dumps(ret)


if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=50052)
